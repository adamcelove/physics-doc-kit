import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import mathml as m  # noqa: E402
import svgarrow  # noqa: E402

DOC = """<html><head><style>body{margin:0}</style></head>
<body><p>Q</p><div class="ans">A</div></body></html>
"""


def parse(fragment):
    # MathML entities are numeric, so the fragment is well-formed XML.
    return ET.fromstring(fragment)


def test_mathml_helpers_produce_valid_markup():
    eq = m.M(m.mi("a"), m.EQ, m.frac(m.DEL + m.mi("v"), m.DEL + m.mi("t")))
    root = parse(eq)
    assert root.tag == "math" and root.get("display") == "inline"
    assert root.find("mfrac") is not None
    block = parse(m.MB(m.subsup(m.mi("v"), m.mi("i"), m.mn("2"))))
    assert block.get("display") == "block" and block.find("msubsup") is not None


def test_paren_is_one_mrow_so_exponent_survives():
    sq = parse(m.M(m.sup(m.paren(m.NEG, m.mn("19.6")), m.mn("2"))))
    msup = sq.find("msup")
    assert msup is not None and len(list(msup)) == 2
    assert list(msup)[0].tag == "mrow"


def test_minus_is_true_minus_and_fn_is_upright():
    assert "&#x2212;" in m.MIN and "-" not in re.sub(r"<[^>]*>", "", m.MIN)
    assert "&#8289;" in m.fn("sin")


def run_toggle(*args):
    return subprocess.run(
        [sys.executable, str(TOOLS / "add-key-toggle.py"), *map(str, args)],
        capture_output=True, text=True,
    )


def test_add_key_toggle_inserts_toggle_and_url_switch(tmp_path):
    f = tmp_path / "ws.html"
    f.write_text(DOC)
    r = run_toggle(f)
    assert r.returncode == 0
    s = f.read_text()
    assert 'id="keybtn"' in s
    assert "body.classList.toggle('key')" in s
    assert "location.search.indexOf('key')" in s
    assert "@media print{#bar{display:none!important}}" in s
    assert "edit-mode" not in s.replace("edit-mode:v1", "") and "contenteditable" not in s


def test_add_key_toggle_is_idempotent(tmp_path):
    f = tmp_path / "ws.html"
    f.write_text(DOC)
    run_toggle(f)
    once = f.read_text()
    r = run_toggle(f)
    assert "skip" in r.stdout
    assert f.read_text() == once
    assert once.count('id="keybtn"') == 1


def test_add_key_toggle_force_refreshes_without_duplicating(tmp_path):
    f = tmp_path / "ws.html"
    f.write_text(DOC)
    run_toggle(f)
    run_toggle(f, "--force")
    s = f.read_text()
    assert s.count('id="keybtn"') == 1
    assert s.count("<script>") == 1


def test_add_key_toggle_resolves_snippets_from_any_cwd(tmp_path):
    f = tmp_path / "ws.html"
    f.write_text(DOC)
    r = subprocess.run(
        [sys.executable, str(TOOLS / "add-key-toggle.py"), str(f)],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert r.returncode == 0 and 'id="keybtn"' in f.read_text()


def test_svgarrow_shaft_stops_at_head():
    h = svgarrow.Head("ah")
    sw = 2.6
    bx, by = h.base(0, 0, 100, 0, sw)
    assert by == 0
    assert bx == pytest.approx(100 - svgarrow.LENGTH * sw)
    line = h.line(0, 0, 100, 0, sw)
    assert 'x2="%.2f"' % bx in line and 'marker-end="url(#ah)"' in line
    assert 'refX="0"' in h.defs()


def test_svgarrow_short_arrow_never_inverts():
    h = svgarrow.Head("ah")
    bx, _ = h.base(0, 0, 5, 0, 2.6)
    assert 0 < bx < 5
