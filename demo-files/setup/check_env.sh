#!/usr/bin/env bash
# Checks a Linux class machine for everything the labs need. Reads only; changes nothing.
# Usage: bash check_env.sh
# Exit code 0 when every REQUIRED item is present, 1 otherwise.

fail=0
ok()   { printf '[ ok ] %s\n' "$1"; }
bad()  { printf '[FAIL] %s\n' "$1"; fail=1; }
warn() { printf '[warn] %s\n' "$1"; }

[ "$(uname -s)" = "Linux" ] && ok "Linux" || warn "Not Linux. The labs are written for Linux class machines."

if command -v python3 >/dev/null 2>&1; then
  if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'; then
    ok "python3 $(python3 -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])')"
  else
    bad "python3 is older than 3.11"
  fi
else
  bad "python3 not found"
fi

command -v jq >/dev/null 2>&1 && ok "jq" || bad "jq not found. Install: sudo apt-get install jq   (or: sudo dnf install jq)"
command -v git >/dev/null 2>&1 && ok "git $(git --version | awk '{print $3}')" || bad "git not found"
command -v claude >/dev/null 2>&1 && ok "claude $(claude --version 2>/dev/null | head -1)" || bad "claude not found on PATH"

if command -v bwrap >/dev/null 2>&1; then ok "bubblewrap (bwrap)"; else bad "bubblewrap not found. Install: sudo apt-get install bubblewrap socat   (or: sudo dnf install bubblewrap socat)"; fi
command -v socat >/dev/null 2>&1 && ok "socat" || bad "socat not found (see the bubblewrap line for the install command)"

if [ -r /proc/sys/kernel/apparmor_restrict_unprivileged_userns ]; then
  v=$(cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns)
  if [ "$v" = "1" ]; then
    warn "kernel.apparmor_restrict_unprivileged_userns = 1. On Ubuntu 24.04 and later this can stop bubblewrap. Ask your instructor for the AppArmor profile fix."
  else
    ok "kernel.apparmor_restrict_unprivileged_userns = $v"
  fi
else
  ok "no AppArmor user namespace restriction setting found (nothing to fix)"
fi

echo
echo "Sandbox probe (run this INSIDE a Claude Code session, with the sandbox on, from the Bash tool):"
echo "  touch ~/sandbox-probe"
echo "Expected with the sandbox working: it fails with 'Read-only file system'."
echo "If it succeeds, remove the file (rm ~/sandbox-probe) and tell your instructor: the sandbox is not active."

[ -n "$ANTHROPIC_API_KEY" ] && warn "ANTHROPIC_API_KEY is set. Claude Code may use it instead of your seat login. Run: unset ANTHROPIC_API_KEY, then /status in Claude Code."

echo
[ $fail -eq 0 ] && echo "All required items present." || echo "Fix the FAIL lines before the labs."
exit $fail
