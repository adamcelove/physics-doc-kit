#!/bin/bash
# printfit auto-check - PostToolUse (Edit|Write|MultiEdit|Bash)
# Runs `printfit check` on a printable HTML whenever it is written directly, or
# after a Bash command runs a builder script (build*.py / make_*.py), in which
# case every HTML that builder produced in the last 2 minutes is checked.
# A failing hard gate exits 2 so the failure is fed back to Claude.
# If jq is missing, exits 0 silently. If printfit is missing, tells the user once
# how to install it and exits 0. Never blocks on its own setup.
# Skips: answer keys, printfit's own output, site/node_modules, non-printable HTML.
set -uo pipefail

command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
tool=$(echo "$input" | jq -r '.tool_name // ""')
TOOLS_DIR="${CLAUDE_PLUGIN_ROOT:-.}/tools"

targets=()
note=""

is_printable() {
  local f="$1"
  case "$f" in
    *.html) ;; *) return 1 ;;
  esac
  case "$f" in
    */printfit/out/*|*/node_modules/*|*/site/*|*/scratchpad/*) return 1 ;;
  esac
  echo "$f" | grep -qiE '(^|[^a-z])key([^a-z]|$)|answer-key|key-variant' && return 1
  [ -f "$f" ] || return 1
  grep -qE '@page|@media print' "$f" || return 1
  return 0
}

if [ "$tool" = "Bash" ]; then
  cmd=$(echo "$input" | jq -r '.tool_input.command // ""')
  script=$(echo "$cmd" | grep -oE '[^ "'"'"']*(build|make)[_-]?[A-Za-z0-9_-]*\.py' | head -1)
  [ -z "$script" ] && exit 0
  cwd=$(echo "$input" | jq -r '.cwd // ""')
  case "$script" in /*) ;; *) script="${cwd:-.}/$script" ;; esac
  dir=$(dirname "$script")
  [ -d "$dir" ] || exit 0
  while IFS= read -r f; do
    is_printable "$f" && targets+=("$f")
  done < <(find "$dir" -maxdepth 3 -name '*.html' -mmin -2 -not -path '*/node_modules/*' 2>/dev/null)
else
  f=$(echo "$input" | jq -r '.tool_input.file_path // ""')
  [ -z "$f" ] && exit 0
  case "$f" in
    *build*.py|*make_*.py)
      msg="Builder script edited: $(basename "$f"). Rebuild now; printfit runs automatically on the HTML it writes. Keep all fixes (including the answer-key toggle) in the builder, never only in the output."
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":$(printf '%s' "$msg" | jq -Rs .)}}"
      exit 0 ;;
  esac
  is_printable "$f" && targets+=("$f")
  # Generated file edited by hand? Warn: a rebuild will wipe it.
  if [ ${#targets[@]} -gt 0 ] && ls "$(dirname "$f")"/*build*.py "$(dirname "$f")"/../*build*.py >/dev/null 2>&1; then
    note="NOTE: a builder script sits next to this HTML. If the HTML is generated, this edit will be lost on rebuild; make it in the builder instead. "
  fi
fi

[ ${#targets[@]} -eq 0 ] && exit 0

if ! command -v printfit >/dev/null 2>&1; then
  state="${PHYSICS_DOC_KIT_STATE_DIR:-${CLAUDE_PLUGIN_DATA:-${TMPDIR:-/tmp}}}"
  flag="$state/physics-doc-kit-printfit-missing"
  if [ ! -e "$flag" ]; then
    mkdir -p "$state" 2>/dev/null && : > "$flag" 2>/dev/null
    msg="physics-doc-kit: printfit is not installed, so printable HTML is not being page-checked. Install it with: uv tool install git+https://github.com/adamcelove/printfit, then reopen the session."
    echo "{\"systemMessage\":$(printf '%s' "$msg" | jq -Rs .)}"
  fi
  exit 0
fi

fails=""
summary=""
for t in "${targets[@]}"; do
  out=$(printfit check "$t" 2>&1)
  verdict=$(echo "$out" | grep -E 'verdict:' | tail -1 | sed 's/.*verdict: *//')
  toggle=""
  grep -qE 'key-toggle:v1|edit-mode:v1' "$t" || toggle=" (no answer-key toggle; if it has answers, add it in the builder, or for a hand-authored file run: python3 $TOOLS_DIR/add-key-toggle.py <file>)"
  if [ -z "$verdict" ]; then
    # printfit crashed or printed nothing parseable: warn, never block on a tool error
    summary+="printfit gave no verdict for $(basename "$t") (tool error, not a layout failure):"$'\n'"$(echo "$out" | tail -5)"$'\n'
  elif [ "$verdict" != "pass" ]; then
    fails+="printfit FAILED on $t${toggle}:"$'\n'"$(echo "$out" | grep -E 'page [0-9]+ +fill|HARD|fix:|verdict' | head -40)"$'\n\n'
  else
    summary+="printfit pass: $(basename "$t")${toggle}"$'\n'"$(echo "$out" | grep -E 'page [0-9]+ +fill')"$'\n'
  fi
done

if [ -n "$fails" ]; then
  printf '%s%s\nFix and re-check until verdict: pass. Never shrink work space to pass (0.30 in/line standard).\n' "$note" "$fails" >&2
  exit 2
fi

msg="${note}${summary}"
echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":$(printf '%s' "$msg" | jq -Rs .)}}"
exit 0
