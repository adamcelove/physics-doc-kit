#!/usr/bin/env python3
"""Fail if any tracked text file matches the denylist (scripts/scrub-denylist.txt)."""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Paths (files or directory prefixes, relative to the root) that are never scanned.
EXEMPT = (
    "scripts/scrub-denylist.txt",
    "scripts/scrub-check.py",
    "tests/test_scrub.py",
)


def load_denylist(path: Path) -> list[re.Pattern]:
    pats = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            pats.append(re.compile(line, re.IGNORECASE))
    return pats


def list_files(root: Path) -> list[str]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard"],
            cwd=root, capture_output=True, text=True, check=True,
        ).stdout
        return [p for p in out.splitlines() if p]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in {".git", ".venv", "__pycache__"}]
            files += [os.path.relpath(os.path.join(dp, f), root) for f in fn]
        return files


def is_exempt(rel: str) -> bool:
    return any(rel == e or (e.endswith("/") and rel.startswith(e)) for e in EXEMPT)


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan(root: Path, denylist: Path | None = None) -> list[str]:
    pats = load_denylist(denylist or root / "scripts" / "scrub-denylist.txt")
    hits = []
    for rel in sorted(list_files(root)):
        if is_exempt(rel):
            continue
        text = read_text(root / rel)
        if text is None:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for p in pats:
                m = p.search(line)
                if m:
                    hits.append(f"{rel}:{n}:{m.group(0)}")
    return hits


def main() -> int:
    hits = scan(ROOT)
    for h in hits:
        print(h)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
