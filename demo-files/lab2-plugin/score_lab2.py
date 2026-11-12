#!/usr/bin/env python3
"""Local scorer for Lab 2 (Build a Plugin With a Hook). No model calls, no organization access.

Usage:
    python3 score_lab2.py PLUGIN_DIR --marketplace MARKETPLACE_DIR [--evidence EVIDENCE_FILE]

Scores 100 points:
    manifest 5, hook wiring 20, hook behavior 15, command 20, agent 10, marketplace 10,
    evidence file 20 (validate output 8, details/always-on cost 6, eval summary 6).
The evidence file is a text file where you paste the output of `claude plugin validate`,
`claude plugin details relnotes` and `claude plugin eval` (see the lab). This scorer only checks
that the evidence is there and plausible. It cannot prove the commands ran.
Standard library only.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

score = 0
lines = []


def award(points, ok, label, detail=""):
    global score
    got = points if ok else 0
    score += got
    lines.append("[%s] %2d/%-2d %s%s" % ("PASS" if ok else "FAIL", got, points, label, ("  -> " + detail) if (detail and not ok) else ""))


def frontmatter(path):
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", text, re.S)
    fields = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln and not ln.startswith((" ", "\t", "-")):
                k, v = ln.split(":", 1)
                fields[k.strip()] = v.strip()
    return fields, text


def main(argv):
    args = list(argv)
    mk = ev = None
    if "--marketplace" in args:
        i = args.index("--marketplace"); mk = Path(args[i + 1]); del args[i:i + 2]
    if "--evidence" in args:
        i = args.index("--evidence"); ev = Path(args[i + 1]); del args[i:i + 2]
    if len(args) != 1:
        print(__doc__); return 2
    root = Path(args[0])

    # 1 manifest (5)
    name = None
    try:
        name = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")).get("name")
    except (OSError, ValueError):
        pass
    award(5, bool(name and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name)), "Manifest has a kebab-case name", "check .claude-plugin/plugin.json")

    # 2 hook wiring (20)
    hooks_path = root / "hooks" / "hooks.json"
    commands = []
    try:
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        commands = [h.get("command", "") for evs in (data.get("hooks") or {}).values() for g in evs for h in g.get("hooks", [])]
    except (OSError, ValueError):
        pass
    award(5, bool(commands), "hooks/hooks.json is valid and defines a command hook")
    award(8, bool(commands) and all("${CLAUDE_PLUGIN_ROOT}" in c for c in commands) and not any(re.search(r"[A-Za-z]:[\\/]|/(home|Users)/", c) for c in commands),
          "Hook command uses ${CLAUDE_PLUGIN_ROOT} and no fixed path on one machine")
    script = None
    for c in commands:
        m = re.search(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)", c)
        if m and (root / m.group(1)).exists():
            script = root / m.group(1)
    award(7, script is not None, "The hook points at a script that exists inside the plugin")

    # 3 hook behavior (15)
    if script:
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d, "RELEASE_NOTES.md"); bad.write_text("TODO write this later\n", encoding="utf-8")
            r1 = subprocess.run([sys.executable, str(script)], input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(bad)}}), capture_output=True, text=True)
            good = Path(d, "RELEASE_NOTES.md")
            good.write_text("# Release notes: v1.1 (since v1.0.0)\n\n## Features\n- Add fuzzy search (#41) (a1b2c3d)\n", encoding="utf-8")
            r2 = subprocess.run([sys.executable, str(script)], input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(good)}}), capture_output=True, text=True)
            other = Path(d, "notes.txt"); other.write_text("TODO\n", encoding="utf-8")
            r3 = subprocess.run([sys.executable, str(script)], input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(other)}}), capture_output=True, text=True)
        award(7, r1.returncode == 2 and r1.stderr.strip() != "", "Bad notes: the hook exits 2 with a message on stderr", "got exit %s" % r1.returncode)
        award(5, r2.returncode == 0, "Good notes: the hook exits 0", "got exit %s" % r2.returncode)
        award(3, r3.returncode == 0, "Other files are ignored: exit 0", "got exit %s" % r3.returncode)
    else:
        award(15, False, "Hook behavior (needs a working script path first)")

    # 4 command (20)
    cmd_files = sorted((root / "commands").glob("*.md")) if (root / "commands").exists() else []
    if cmd_files:
        fm, text = frontmatter(cmd_files[0])
        award(4, "TODO" not in text, "Command has no TODO left")
        award(4, len(fm.get("description", "")) >= 40, "Command description is specific (40+ characters)")
        award(4, "RELEASE_NOTES.md" in text and "changelog-auditor" in text, "Command names RELEASE_NOTES.md and the changelog-auditor agent")
        order = [text.find(s) for s in ("Breaking changes", "Features", "Fixes", "Other changes")]
        award(4, all(o >= 0 for o in order) and order == sorted(order), "Command states the four sections in order")
        award(4, re.search(r"never invent|do not invent|not invent", text, re.I) is not None and re.search(r"nothing except|only .*RELEASE_NOTES", text, re.I) is not None,
              "Command forbids inventing entries and limits changes to RELEASE_NOTES.md")
    else:
        award(20, False, "Command file exists in commands/")

    # 5 agent (10)
    agent_files = sorted((root / "agents").glob("*.md")) if (root / "agents").exists() else []
    if agent_files:
        fm, _ = frontmatter(agent_files[0])
        tools = {t.strip().split("(")[0] for t in fm.get("tools", "").split(",") if t.strip()}
        award(10, bool(tools) and not (tools & {"Edit", "Write", "Bash", "NotebookEdit"}), "The checking agent has read-only tools", "tools = %s" % sorted(tools))
    else:
        award(10, False, "Agent file exists in agents/")

    # 6 marketplace (10)
    ok_mk = False
    if mk and name:
        try:
            entries = json.loads((mk / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")).get("plugins", [])
            for e in entries:
                src = e.get("source")
                if e.get("name") == name and isinstance(src, str) and ".." not in src and (mk / src / ".claude-plugin" / "plugin.json").exists():
                    ok_mk = True
        except (OSError, ValueError):
            pass
    award(10, ok_mk, "Marketplace entry name matches the manifest and its source path holds the plugin", "pass --marketplace DIR; entry name must equal the manifest name")

    # 7 evidence (20)
    text = ev.read_text(encoding="utf-8", errors="replace") if ev and ev.exists() else ""
    award(8, bool(re.search(r"claude plugin validate", text)) and bool(re.search(r"(passed|valid|success|no errors|exit(ed)? (code )?0)", text, re.I)), "Evidence: validate output pasted and it passed")
    award(6, bool(re.search(r"(always-on|projected token cost|token cost)", text, re.I)), "Evidence: plugin details output with the token cost pasted")
    award(6, bool(re.search(r"claude plugin eval", text)) and bool(re.search(r"(pass|fail|threshold|aggregate-result|report\.html)", text, re.I)), "Evidence: eval run summary pasted")

    print("LAB 2 SCORE (local checks)")
    print("\n".join(lines))
    print("\nTOTAL: %d / 100" % score)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
