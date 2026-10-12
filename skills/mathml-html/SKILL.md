---
name: mathml-html
description: Render every equation in an HTML deliverable as native MathML instead of plain-text or sub/sup markup. Use whenever writing or editing an HTML file (worksheet, key, handout, reference card, quiz, lab) that contains a formula, equation, fraction, subscripted variable, exponent, square root, or vector symbol.
---

# MathML in HTML

Formulas in HTML deliverables are native MathML: never plain text, never `<sub>`/`<sup>` fakery, never an image, never a MathJax or KaTeX script. MathML renders in current Safari, Chrome, and Firefox, prints correctly, stays selectable, and is screen-reader readable. The rules around equations in solutions are in `${CLAUDE_PLUGIN_ROOT}/standards/solution-writing.md`, section 9.

## Rules

1. Every displayed equation is a `<math>` element. A lone variable in prose may stay `<i>v</i>`; anything with an operator, fraction, exponent, subscript, or radical becomes MathML.
2. No CDN math libraries and no `<script src=...>`. Documents render offline.
3. Build markup with the helper library `${CLAUDE_PLUGIN_ROOT}/tools/mathml.py` (copy it into the project's build directory or import it): `M()`, `mi()`, `mn()`, `mo()`, `frac()`, `sub()`, `sup()`, `subsup()`, `sqrt()`, `vec()`, `mag()`, `fn()`, `paren()`. For a hand-written file, follow `${CLAUDE_PLUGIN_ROOT}/skills/mathml-html/reference/mathml-cheatsheet.md` exactly.
4. One semantic element per token: `<mi>` variables, `<mn>` numbers, `<mo>` operators. Units are `<mtext>`, not `<mi>`.
5. Minus is U+2212 (`&#x2212;`), not a hyphen. Delta is upright (`<mi mathvariant='normal'>&#x394;</mi>`).
6. Function names (`sin`, `cos`, `tan`) use `fn("sin")` so they render upright with an invisible apply.
7. Give `math` a font stack and size in the stylesheet (see `tools/mathml.py`, the `CSS` constant), or it inherits the body font and looks wrong.
8. `display="inline"` for equations in a row or label grid; `display="block"` only for a centered standalone equation.
9. `paren()` returns an `<mrow>`; keep it that way, or `msup` silently drops the exponent. Check that exponents on parenthesized quantities render raised.
10. Prose around equations follows `${CLAUDE_PLUGIN_ROOT}/standards/physics-language.md`.

## Verify

Open the file and confirm no equation fell back to raw tag text, then run `printfit check <abs-path>` on the blank state (MathML changes line heights, so page counts shift).
