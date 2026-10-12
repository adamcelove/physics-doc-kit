import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HOOKS = ROOT / "hooks"

pytestmark = pytest.mark.skipif(shutil.which("jq") is None, reason="jq not installed")

NEEDED = ["jq", "grep", "sed", "find", "ls", "dirname", "basename", "cat",
          "printf", "tr", "head", "tail", "mkdir", "bash"]


def bin_dir(tmp_path, with_printfit=None, with_jq=True):
    """A PATH holding only basic tools, optionally a stub printfit."""
    b = tmp_path / "bin"
    b.mkdir(exist_ok=True)
    for name in NEEDED:
        if name == "jq" and not with_jq:
            continue
        src = shutil.which(name)
        if src and not (b / name).exists():
            (b / name).symlink_to(src)
    if with_printfit:
        p = b / "printfit"
        p.write_text("#!/bin/bash\n" + with_printfit + "\n")
        p.chmod(0o755)
    return b


def run(hook, payload, tmp_path, **kw):
    b = bin_dir(tmp_path, kw.get("printfit"), kw.get("jq", True))
    env = {"PATH": str(b), "PHYSICS_DOC_KIT_STATE_DIR": str(tmp_path / "state"),
           "CLAUDE_PLUGIN_ROOT": str(ROOT), "HOME": str(tmp_path)}
    return subprocess.run(["/bin/bash", str(HOOKS / hook)], input=json.dumps(payload),
                          capture_output=True, text=True, env=env)


def write(path, content):
    return {"tool_name": "Write", "tool_input": {"file_path": str(path), "content": content}}


# ---- mathml-pretool.sh ----

def test_equation_without_math_warns(tmp_path):
    r = run("mathml-pretool.sh", write("a.html", "<p>v = d/t, v<sub>f</sub></p>"), tmp_path)
    assert r.returncode == 0
    assert "mathml-html" in json.loads(r.stdout)["systemMessage"]


def test_equation_with_math_is_silent(tmp_path):
    r = run("mathml-pretool.sh", write("a.html", "<math><mi>v</mi><mo>=</mo><mi>d</mi></math> v = d"), tmp_path)
    assert r.returncode == 0 and r.stdout == ""


def test_non_html_is_silent(tmp_path):
    r = run("mathml-pretool.sh", write("a.py", "v = d / t"), tmp_path)
    assert r.returncode == 0 and r.stdout == ""


def test_multiedit_payload_is_scanned(tmp_path):
    payload = {"tool_name": "MultiEdit", "tool_input": {
        "file_path": "a.html", "edits": [{"old_string": "x", "new_string": "t&sup2;"}, {"old_string": "y", "new_string": "<sup>2</sup>"}]}}
    r = run("mathml-pretool.sh", payload, tmp_path)
    assert "systemMessage" in r.stdout


def test_mathml_hook_exits_silently_without_jq(tmp_path):
    r = run("mathml-pretool.sh", write("a.html", "v = d/t"), tmp_path, jq=False)
    assert r.returncode == 0 and r.stdout == ""


# ---- printfit-key-guard.sh ----

def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def test_key_guard_warns_on_key_file(tmp_path):
    r = run("printfit-key-guard.sh", bash("printfit check /x/unit1-answer-key.html"), tmp_path)
    assert r.returncode == 0 and "not run on answer keys" in json.loads(r.stdout)["systemMessage"]


def test_key_guard_silent_on_worksheet_and_other_commands(tmp_path):
    assert run("printfit-key-guard.sh", bash("printfit check /x/ws.html"), tmp_path).stdout == ""
    assert run("printfit-key-guard.sh", bash("ls key.html"), tmp_path).stdout == ""


def test_key_guard_without_jq(tmp_path):
    r = run("printfit-key-guard.sh", bash("printfit check k-key.html"), tmp_path, jq=False)
    assert r.returncode == 0 and r.stdout == ""


# ---- printfit-posttool.sh ----

PRINTABLE = "<html><style>@page{size:letter}</style><body><p>hi</p></body></html>"


def make_printable(tmp_path, name="ws.html"):
    f = tmp_path / "docs" / name
    f.parent.mkdir(exist_ok=True)
    f.write_text(PRINTABLE)
    return f


def test_missing_printfit_prints_install_message_once(tmp_path):
    f = make_printable(tmp_path)
    r = run("printfit-posttool.sh", write(f, PRINTABLE), tmp_path)
    assert r.returncode == 0
    assert "uv tool install git+https://github.com/adamcelove/printfit" in json.loads(r.stdout)["systemMessage"]
    again = run("printfit-posttool.sh", write(f, PRINTABLE), tmp_path)
    assert again.returncode == 0 and again.stdout == ""


def test_posttool_pass_reports_summary(tmp_path):
    f = make_printable(tmp_path)
    stub = "echo 'page 1 fill 80%'; echo 'verdict: pass'"
    r = run("printfit-posttool.sh", write(f, PRINTABLE), tmp_path, printfit=stub)
    assert r.returncode == 0
    ctx = json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "printfit pass: ws.html" in ctx and "add-key-toggle.py" in ctx


def test_posttool_fail_exits_2(tmp_path):
    f = make_printable(tmp_path)
    stub = "echo 'HARD overflow'; echo 'verdict: fail'"
    r = run("printfit-posttool.sh", write(f, PRINTABLE), tmp_path, printfit=stub)
    assert r.returncode == 2 and "printfit FAILED" in r.stderr


def test_posttool_skips_keys_and_non_printables(tmp_path):
    key = make_printable(tmp_path, "unit1-key.html")
    plain = tmp_path / "plain.html"
    plain.write_text("<p>no print css</p>")
    for f in (key, plain):
        r = run("printfit-posttool.sh", write(f, "x"), tmp_path, printfit="echo 'verdict: fail'")
        assert r.returncode == 0 and r.stdout == ""


def test_posttool_builder_edit_reminds_to_rebuild(tmp_path):
    payload = write(tmp_path / "build_ws.py", "print(1)")
    r = run("printfit-posttool.sh", payload, tmp_path)
    assert "Rebuild now" in json.loads(r.stdout)["hookSpecificOutput"]["additionalContext"]


def test_posttool_without_jq(tmp_path):
    f = make_printable(tmp_path)
    r = run("printfit-posttool.sh", write(f, PRINTABLE), tmp_path, jq=False)
    assert r.returncode == 0 and r.stdout == ""


def test_hooks_json_registers_all_scripts():
    cfg = json.loads((HOOKS / "hooks.json").read_text())["hooks"]
    cmds = json.dumps(cfg)
    for h in ("mathml-pretool.sh", "printfit-key-guard.sh", "printfit-posttool.sh"):
        assert h in cmds and (HOOKS / h).exists()
