#!/usr/bin/env python3
"""Rebuild demos.md from demos/*.md, so the printable copy cannot drift.

    python3 testing/build_demos_md.py          rewrite demos.md
    python3 testing/build_demos_md.py --check  exit 1 if it is stale, change nothing

demos/ holds one file per demo and demos.md is a single printable copy of all ten.
Keeping both by hand failed exactly as you would expect: a 2026-11-14 fix corrected the
AppArmor claim in demos/demo-9-*.md and left demos.md still saying the profile is "off
by default" - the opposite of the class image - which the RVC run then found.

demos/ is the source. This regenerates the copy. Run --check in CI or before a release.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "demos")
OUT = os.path.join(REPO, "demos.md")

PREAMBLE_END = "## The demos"


def demo_files():
    def num(name):
        m = re.match(r"demo-(\d+)-", name)
        return int(m.group(1)) if m else 999
    names = [n for n in os.listdir(SRC) if n.endswith(".md") and n != "README.md"]
    return [os.path.join(SRC, n) for n in sorted(names, key=num)]


def body_of(path):
    """Strip the per-file nav header the split added; keep the demo itself."""
    text = open(path, encoding="utf-8").read()
    parts = text.split("\n---\n", 1)
    body = parts[1] if len(parts) > 1 else text
    return body.strip()


def title_of(path):
    first = open(path, encoding="utf-8").readline().strip()
    return first.lstrip("# ").strip()


def build():
    readme = open(os.path.join(SRC, "README.md"), encoding="utf-8").read()
    preamble = readme.split(PREAMBLE_END)[0].rstrip()
    preamble = preamble.replace("# Demos", "# AI Champions Training: Claude Code for Engineering Teams. Demos", 1)

    chunks = [preamble, "", "> Generated from `demos/` by `testing/build_demos_md.py`. Edit the files in",
              "> `demos/`, not this copy, then regenerate.", ""]
    for p in demo_files():
        chunks += ["---", "", "## " + title_of(p), "", body_of(p), ""]
    return "\n".join(chunks).rstrip() + "\n"


def main():
    new = build()
    current = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if "--check" in sys.argv:
        if new == current:
            print("demos.md is current")
            return 0
        print("demos.md is STALE - demos/ has changed since it was generated.")
        print("Regenerate with: python3 testing/build_demos_md.py")
        return 1
    open(OUT, "w", encoding="utf-8", newline="\n").write(new)
    print("wrote demos.md from %d files in demos/" % len(demo_files()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
