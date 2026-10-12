import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "scrub_check", Path(__file__).resolve().parent.parent / "scripts" / "scrub-check.py"
)
scrub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scrub)


def make(tmp_path, files, deny="/Users/\n(?-i:\\bLove\\b)\nBlackbaud\n"):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "scrub-denylist.txt").write_text("# c\n" + deny)
    for name, content in files.items():
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content)
    return tmp_path


def test_hit_reports_file_line_match(tmp_path):
    root = make(tmp_path, {"a.md": "ok\nsee /Users/bob/x\n"})
    assert scrub.scan(root) == ["a.md:2:/Users/"]


def test_clean_tree(tmp_path):
    root = make(tmp_path, {"a.md": "nothing here\n", "b.txt": "I love physics\n"})
    assert scrub.scan(root) == []


def test_case_sensitive_inline_flag(tmp_path):
    root = make(tmp_path, {"a.md": "Love wins\n"})
    assert len(scrub.scan(root)) == 1


def test_exempt_paths(tmp_path):
    root = make(tmp_path, {
        "scripts/scrub-check.py": "/Users/\n",
        "tests/test_scrub.py": "Blackbaud\n",
        "scripts/scrub-denylist.txt": "Blackbaud\n",
    })
    assert scrub.scan(root) == []


def test_binary_skipped(tmp_path):
    root = make(tmp_path, {"img.png": b"\x00\x01Blackbaud\x00"})
    assert scrub.scan(root) == []
