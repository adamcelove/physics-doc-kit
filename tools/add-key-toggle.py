#!/usr/bin/env python3
"""Add the answer-key toggle to an HTML document.

    python3 add-key-toggle.py path/to/doc.html [more.html ...]

Adds a single fixed, screen-only button that flips `body.key`, plus the `?key`
URL switch. The button hides itself in a document with no `.ans` element and
never prints. Idempotent: a document that already carries the toggle is left
alone, and --force replaces it with the current snippet.
"""
import pathlib
import re
import sys

SNIPPETS = pathlib.Path(__file__).resolve().parent / "key-toggle"
MARKS = ("key-toggle:v1", "edit-mode:v1")  # edit-mode:v1 marks older copies


def snippet(ext):
    return (SNIPPETS / f"snippet.{ext}").read_text()


def has_toggle(s):
    return any(m in s for m in MARKS)


def strip(s):
    """Remove an existing toggle (CSS, button, script) so it can be refreshed."""
    s = re.sub(r"\n?/\* (?:key-toggle|edit-mode):v1 \*/.*?(?=</style>)", "", s, flags=re.S)
    s = re.sub(r'<!-- (?:key-toggle|edit-mode):v1 -->\s*(?:</head>\s*<body[^>]*>\s*)?'
               r'<div id="bar">.*?</div>\n?', "", s, flags=re.S)
    s = re.sub(r"<script>\n\(function\(\)\{\nvar \$=function\(q\).*?</script>\n?", "", s, flags=re.S)
    return s


def inject(s):
    css, bar, js = snippet("css"), snippet("html"), snippet("js")
    if "</style>" in s:
        s = s.replace("</style>", "\n" + css + "</style>", 1)
    else:
        s = "<style>\n" + css + "</style>\n" + s
    s = s.replace("</style>", "</style>\n" + bar, 1)
    if "</body>" in s:
        s = s.replace("</body>", js + "</body>", 1)
    else:
        s = s.rstrip("\n") + "\n\n" + js
    return s


def main(argv):
    force = "--force" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 1
    for f in files:
        p = pathlib.Path(f)
        s = p.read_text()
        if has_toggle(s) and not force:
            print(f"skip (already has the toggle): {f}")
            continue
        if has_toggle(s):
            s = strip(s)
        p.write_text(inject(s))
        print(f"added answer-key toggle: {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
