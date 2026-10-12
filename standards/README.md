# standards/

The physics authoring rules, in prose. Skills state the binding rules tersely and load these files for the detail. Each file is self-contained: it states a rule, says why, and shows right and wrong.

| File | Covers |
|---|---|
| `physics-language.md` | Banned motion words, describing acceleration by signs, same/opposite, direction words with signs, sign conventions as the student's choice, kinematic equations, F_g, opposite/adjacent trig, base-equations-only sheets, state-don't-ask-to-justify, no em dashes |
| `solution-writing.md` | Keys as toggles and screen documents, symbolic before numbers with units, two figures per solution placed before part (a), deriving symmetry, the quadratic calculator path, MathML, key layout, handback checklist |
| `workspace-sizing.md` | Blank unruled space, 0.30 in per line sizing, drawing-first parts, FBD plus force sums for forces problems, floors and fill, three big subquestions per test page |
| `worksheet-anatomy.md` | Intro page, situation in Part 1, sections at page top, questions never split, break mechanics, what the print check can and cannot catch, verify loop |
| `diagrams.md` | Numbered scales and units on graph axes, explicit SVG sizing, arrow shafts, labels and subscript baselines, role colors, motion and interaction diagrams, render-and-look |
| `answer-key-toggle.md` | `.ans` and `body.key`, the `?key` switch, larger answer text, keys never print-checked, when not to add the toggle |

## Loading map

| Skill | Loads |
|---|---|
| `worksheet` | `worksheet-anatomy.md`, `workspace-sizing.md`, `diagrams.md`, `answer-key-toggle.md`, `physics-language.md` |
| `solution-keys` | `solution-writing.md`, `answer-key-toggle.md`, `diagrams.md`, `physics-language.md` |
| `mathml-html` | `solution-writing.md` (section 9 only) |

Any prose about motion, in any skill, follows `physics-language.md`.
