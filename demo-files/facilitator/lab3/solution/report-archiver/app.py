"""report-archiver (fixed). The report name is validated and passed as an argument list, never through a shell."""
import re
import subprocess
import sys

NAME = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]*$")


def checksum_report(name):
    if not NAME.match(name):
        raise ValueError("invalid report name: %r" % name)
    return subprocess.run([sys.executable, "tools/checksum.py", name]).returncode


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 app.py <report-file-name>")
        sys.exit(2)
    try:
        sys.exit(checksum_report(sys.argv[1]))
    except ValueError as exc:
        print(exc)
        sys.exit(2)
