---
name: worksheet
description: Build or edit a printable physics worksheet, quiz, test, lab handout, or answer key (HTML). Use for any new printable or any change to an existing one. Encodes the builder-only edit rule, workspace sizing, FBD-first, answer-key toggle, diagram conventions, and the printfit verification loop.
---

# Worksheet

A hook runs `printfit check` automatically on every printable HTML you write and after every `build*.py` or `make_*.py` run. A failing hard gate comes back to you as a blocking error. Fix it; never ignore it. (If `printfit` is not installed, the hook tells the user once and does nothing else.)

Load these standards before writing (paths relative to `${CLAUDE_PLUGIN_ROOT}/standards/`):

- `worksheet-anatomy.md`: intro page, situation in Part 1, sections at page top, questions never split
- `workspace-sizing.md`: 0.30 in per line, blank unruled space, floors and fill
- `diagrams.md`: axis scales and units, SVG sizing, arrows, labels
- `answer-key-toggle.md`: `.ans`, `body.key`, `?key`
- `physics-language.md`: banned motion words, sign wording, notation

## Must-do checklist

1. **Find the source of truth.** If a builder script (`build*.py`, `make_*.py`) sits next to or above the target HTML, edit only the builder and rebuild. Edits to generated HTML are lost on the next build, including the answer-key toggle.
2. **Size work space by the standard.** Never shrink work space to make printfit pass.
3. **Forces problems** open with an FBD box, then the sum of forces equals ma, then the algebra.
4. **Equations are MathML.** Load the `mathml-html` skill.
5. **Motion language** follows `physics-language.md`: no "forward", "backward", "decelerate"; describe acceleration by sign, relation to the velocity's sign, and the result.
6. **Graphs and grids** get a numbered scale and units on both axes, unless choosing the scale is the skill being practiced.
7. **Answer key** is a toggle on the same document, never a second file. In a builder, emit it from the builder. For a hand-authored file, run `python3 ${CLAUDE_PLUGIN_ROOT}/tools/add-key-toggle.py <file.html>`. Load the `solution-keys` skill before writing any solution.
8. **Every SVG has an explicit `height`**; when a figure shrinks, scale its in-SVG `font-size` up so nothing drops below 7px. Shaded cells that must print need `print-color-adjust:exact` inside `@media print`.
9. If rendering is wrong on a target platform, simplify the markup. Never delete a table, figure, or question to make a problem go away.

## Verify (loop until clean, at most 5 rounds)

1. Rebuild or write the file. The hook runs printfit. Iterate until `verdict: pass`. To run it by hand: `printfit check <abs-path>`.
2. Check the blank state only. Never run printfit on the key state, never inject `<body class="key">` into a scratch copy, never compress key layout to paginate.
3. Render every page in the blank state (for example `printfit render <abs-path>`, or headless Chromium) and look for overlapping labels, clipped figures, and overflow.
4. Fix in the builder and repeat.

## Hand back

Open the final HTML for the user. Report the page and fill table from printfit, the page count, and whether the answer-key toggle is present (if the document has answers).
