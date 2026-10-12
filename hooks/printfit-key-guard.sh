#!/bin/bash
# printfit key guard - PreToolUse (Bash)
# printfit is for PRINTABLES. Warn when a printfit run targets an answer-key
# state (a *key*.html path, or a scratch copy with body class="key" injected).
# If jq is missing, exits 0 silently.
set -euo pipefail

command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // ""')
[ -z "$cmd" ] && exit 0

echo "$cmd" | grep -q 'printfit' || exit 0
echo "$cmd" | grep -qiE '[^a-z]key[^a-z]*\.html|key-variant|-key\.html|answer-key' || exit 0

msg="printfit is not run on answer keys, only on printable worksheets. A key is read on a screen; page count is not a constraint on it, and key layout must never be compressed to paginate. Check the blank worksheet state instead and report its page/fill table."
echo "{\"systemMessage\":$(printf '%s' "$msg" | jq -Rs .)}"
exit 0
