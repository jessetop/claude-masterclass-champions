#!/usr/bin/env python3
"""Static settings checker for Lab 3. Works on any machine: it reads files and runs nothing.

Usage:  python3 check_settings.py PATH_TO_PROJECT      (for example ~/work/report-archiver)
Reads PATH_TO_PROJECT/.claude/settings.json, .mcp.json, app.py and any script a hook names.

Scores 60 points (Part A). Part B is the live attack script (40 points, attack_simulation.py).
It also prints the attack outcomes the configuration PREDICTS. A prediction is not an observation:
only the live script run inside a Claude Code session, with the sandbox active, shows what really happens.

Unconfirmed items (not in the class facts file, so treated as scenario conventions):
  - The exact entry format for sandbox.excludedCommands. This checker passes it when the list is empty or absent.
  - How a relative path in sandbox.filesystem is resolved. This checker only looks for the words
    "secrets" and ".ssh" in denyRead entries.
Standard library only.
"""
import json
import os
import re
import sys

APPROVED_DOMAINS = {"pypi.org", "files.pythonhosted.org", "api.example.com"}
APPROVED_SERVERS = {"docs-search", "ticket-bridge"}
BROAD_WRITE = {"~", "/", "*", "..", "../", "$home", "%userprofile%", "~/", "**"}
NETWORK_WORDS = re.compile(r"urllib|requests|http\.client|socket|curl|wget|urlopen")


def low(s):
    return str(s).strip().lower()


def find(obj, key):
    """Return the first value for key anywhere inside obj, else None."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            r = find(v, key)
            if r is not None:
                return r
    return None


def flat(items):
    return [low(x) for x in (items or []) if isinstance(x, str)]


def hook_commands(cfg):
    out = []
    for groups in (cfg.get("hooks") or {}).values():
        for g in groups if isinstance(groups, list) else []:
            for h in g.get("hooks", []):
                if isinstance(h, dict) and h.get("command"):
                    out.append(h["command"])
    return out


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    root = sys.argv[1]
    try:
        with open(os.path.join(root, ".claude", "settings.json"), encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError) as exc:
        print("Cannot read .claude/settings.json: %s" % exc)
        sys.exit(1)
    sb = cfg.get("sandbox", {}) if isinstance(cfg.get("sandbox"), dict) else {}
    perms = cfg.get("permissions", {}) if isinstance(cfg.get("permissions"), dict) else {}
    deny = flat(perms.get("deny"))
    allow = flat(perms.get("allow"))
    rows = []

    def check(label, pts, ok, detail):
        rows.append((label, pts, pts if ok else 0, detail))

    enabled = sb.get("enabled") is True
    check("sandbox.enabled is true", 7, enabled, "sandbox.enabled = %r" % sb.get("enabled"))
    check("sandbox.failIfUnavailable is true", 7, sb.get("failIfUnavailable") is True,
          "failIfUnavailable = %r (the default is to run WITHOUT a sandbox when it cannot start)" % sb.get("failIfUnavailable"))
    excl = sb.get("excludedCommands")
    check("sandbox.excludedCommands is empty or absent (nothing runs outside the sandbox on purpose)", 5, not excl,
          "excludedCommands = %r (those commands run outside the sandbox)" % excl)

    domains = find(sb, "allowedDomains")
    dl = flat(domains)
    bad = [d for d in dl if d not in APPROVED_DOMAINS]
    check("network.allowedDomains is a non-empty list of approved domains only", 7,
          bool(dl) and not bad, "allowedDomains = %r; not approved: %r" % (domains, bad))

    aw = find(sb, "allowWrite")
    awl = flat(aw)
    broad = [x for x in awl if x in BROAD_WRITE or x.startswith("~") or (x.startswith("/") and len(x) <= 5)]
    check("filesystem.allowWrite grants no broad path (home, root, parent)", 5, not broad,
          "allowWrite = %r; too broad: %r" % (aw, broad))
    dr = flat(find(sb, "denyRead"))
    sec = any("secrets" in x for x in dr)
    ssh = any(".ssh" in x for x in dr)
    check("sandbox filesystem.denyRead covers the secrets file and ~/.ssh (this covers shell commands)", 5, sec and ssh,
          "denyRead = %r (secrets file: %s, ssh: %s)" % (dr, sec, ssh))
    dw = flat(find(sb, "denyWrite"))
    check("filesystem.denyWrite protects .claude and .mcp.json", 3,
          any(".claude" in x for x in dw) and any(".mcp.json" in x for x in dw), "denyWrite = %r" % dw)

    check("permissions.deny has Read rules for the secrets file and .env (this covers Claude's file tools)", 4,
          any(x.startswith("read") and "secrets" in x for x in deny) and any(x.startswith("read") and ".env" in x for x in deny),
          "deny = %r" % deny)
    check("permissions.deny blocks curl and wget", 3,
          any("curl" in x for x in deny) and any("wget" in x for x in deny), "deny = %r" % deny)
    blanket = [x for x in allow if x in ("bash", "bash(*)", "bash(*:*)", "*")]
    check("permissions.allow has no blanket Bash allow", 4, not blanket, "blanket allow rules: %r" % blanket)

    try:
        with open(os.path.join(root, ".mcp.json"), encoding="utf-8") as f:
            declared = set(json.load(f).get("mcpServers", {}).keys())
    except (OSError, ValueError):
        declared = set()
    check("MCP: .mcp.json declares only approved servers (docs-search, ticket-bridge)", 6,
          bool(declared) and declared <= APPROVED_SERVERS,
          "declared in .mcp.json = %r; not approved: %r" % (sorted(declared), sorted(declared - APPROVED_SERVERS)))

    net_hooks = []
    for cmd in hook_commands(cfg):
        for token in re.findall(r"[\w./${}-]+\.py", cmd):
            path = token.replace("${CLAUDE_PROJECT_DIR}", root)
            path = path if os.path.isabs(path) else os.path.join(root, path)
            try:
                with open(path, encoding="utf-8") as f:
                    if NETWORK_WORDS.search(f.read()):
                        net_hooks.append(token)
            except OSError:
                pass
    check("hooks: no hook script reaches the network (hooks run OUTSIDE the sandbox)", 4, not net_hooks,
          "hook scripts with network calls: %r" % net_hooks)

    total = 0
    print("PART A: static checklist")
    for label, pts, got, detail in rows:
        total += got
        print("  [%s] %2d/%-2d %s" % ("PASS" if got else "FAIL", got, pts, label))
        if not got:
            print("            %s" % detail)
    print("  PART A SCORE: %d / 60\n" % total)

    net_ok = enabled and bool(dl) and "*" not in dl
    read_ok = enabled and sec
    write_ok = enabled and not broad
    try:
        with open(os.path.join(root, "app.py"), encoding="utf-8") as f:
            vulnerable = "os.system(" in f.read()
    except OSError:
        vulnerable = True
    print("PREDICTED attack outcomes (a prediction, not an observation)")
    print("  1 write outside the working directory : %s" % ("blocked if the sandbox starts" if write_ok else "will succeed"))
    print("  2 disallowed destination              : %s" % ("blocked if the sandbox starts" if net_ok else "will succeed"))
    print("  3 read the secrets file from a script : %s" % ("blocked if the sandbox starts" if read_ok else "will succeed"))
    print("  4 command injection in app.py         : %s" % (
        "will succeed: app.py still builds a shell command, and a sandbox does not stop a command inside the working directory" if vulnerable
        else "no os.system found in app.py"))
    print("  Hook scripts and MCP servers are not limited by the sandbox, so the checklist reads them instead.")


if __name__ == "__main__":
    main()
