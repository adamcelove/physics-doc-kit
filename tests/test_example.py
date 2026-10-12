import shutil
import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "horizontal-launch"


@pytest.fixture(scope="module")
def html():
    subprocess.run([sys.executable, str(EXAMPLE / "build.py")], check=True, cwd=EXAMPLE)
    return (EXAMPLE / "worksheet.html").read_text(encoding="utf-8")


def test_build_emits_mathml_and_key_toggle(html):
    assert "<math" in html
    assert "key-toggle:v1" in html and 'id="keybtn"' in html
    assert "location.search.indexOf('key')" in html


def test_every_part_has_answer_and_both_figures(html):
    assert html.count('class="ans"') == 6
    assert html.count('class="figs"') == 2
    assert html.count('data-fig-role="graph"') == 2


def test_no_banned_wording(html):
    low = html.lower()
    for bad in ("forward", "backward", "decelerat", "—", "&mdash;", "&#8212;"):
        assert bad not in low


def test_printfit_passes_on_blank_state():
    if shutil.which("printfit") is None:
        pytest.skip("printfit not on PATH")
    r = subprocess.run(["printfit", "check", str(EXAMPLE / "worksheet.html"), "--out",
                        str(EXAMPLE.parent.parent / "out")],
                       capture_output=True, text=True)
    assert "verdict: pass" in r.stdout
