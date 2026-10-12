#!/bin/bash
# MathML hook - PreToolUse (Write|Edit|MultiEdit)
# Fires when an HTML file is written with equation-looking content that is NOT
# already MathML, and tells Claude to load the mathml-html skill.
# If jq is missing, exits 0 silently.
set -euo pipefail

command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)

file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""')
[ -z "$file_path" ] && exit 0

case "$(echo "$file_path" | tr '[:upper:]' '[:lower:]')" in
  *.html|*.htm) ;;
  *) exit 0 ;;
esac

# The text being written: Write.content, Edit.new_string, MultiEdit edits[].new_string
payload=$(echo "$input" | jq -r '
  [ (.tool_input.content // empty),
    (.tool_input.new_string // empty),
    ((.tool_input.edits // []) | map(.new_string // "") | join("\n")) ]
  | join("\n")')
[ -z "$payload" ] && exit 0

# Already MathML: nothing to nag about.
echo "$payload" | grep -qi '<math' && exit 0

# Equation signals: fake sub/sup, unicode math, or a bare "x = y" formula.
if echo "$payload" | grep -qiE \
   '<sub>|<sup>|&Delta;|[ΔΣθπμω√±≈∝×÷°]|&[a-zA-Z]+;?[²³]|[²³]|[a-zA-Z_]\)? ?= ?[-0-9a-zA-Z(½Δ]|&frac|&radic|&times;|&divide;'
then
  echo '{"systemMessage":"This HTML file contains equation-like content that is not MathML. Every formula in an HTML deliverable must be native MathML (no <sub>/<sup> fakery, no MathJax/KaTeX CDN, no images). Load the mathml-html skill before writing the equations."}'
fi
exit 0
