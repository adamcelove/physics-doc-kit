# Walkthrough: decision to rule

| Decision in the example | Standard |
|---|---|
| One `worksheet.html`; answers are `.ans` blocks shown by `body.key`, button plus `?key` | `answer-key-toggle.md` 1, `solution-writing.md` 1 |
| Toggle injected by the builder from `tools/key-toggle`, so a rebuild never drops it | `answer-key-toggle.md` 4, `worksheet-anatomy.md` 7 |
| Print check run on the blank state only; no check of the key | `solution-writing.md` 2, `answer-key-toggle.md` 3 |
| Key text 12 pt against 11 pt questions, generous spacing between steps | `answer-key-toggle.md` 2, `solution-writing.md` 10 |
| Page 1 is general information only; the cliff first appears in Part 1 | `worksheet-anatomy.md` 1, 2 |
| Each Part starts at the top of a page; each question is one `.qbox` | `worksheet-anatomy.md` 3, 4, 5 |
| Pagination read page by page after the print check passed | `worksheet-anatomy.md` 6, 8 |
| Blank space, no answer lines; height = 0.30 in x lines + 0.25 in, rounded up | `workspace-sizing.md` 1, 2, 9 |
| Each part sized by its own line count; `sp(lines)` in the builder. A calculation is never below 4 lines (1.5 in); 1(c) is 13 lines (speed, angle, and the vertical component first), the last part on its page, so 0.5 in short | `workspace-sizing.md` 2, 4, 5, 9 |
| Leftover room goes to the spaces, last part may be 0.5 in short | `workspace-sizing.md` 5 |
| Intro tells students to choose a positive direction; no convention is stated | `physics-language.md` 5 |
| Key opens each answer with "I chose right as positive for x and up as positive for y" | `solution-writing.md` 4, `physics-language.md` 5 |
| Every signed value has a direction word: "(downward)", "(right)" | `physics-language.md` 4 |
| Calculations run EQUATION, SOLVE FOR THE UNKNOWN, PLUG-IN; solve step skipped when the equation already solves | `solution-writing.md` 3 |
| Units inside the plug-in parentheses: (12.0 m/s)(3.03 s) | `solution-writing.md` 3 |
| Final value highlighted, nothing else | `solution-writing.md` 3, 10 |
| Plug-in uses the rounded intermediate shown; the builder asserts it gives the same answer | `solution-writing.md` 3 |
| Angle found from opposite over adjacent, never "cos is x" | `physics-language.md` 8 |
| Two figures before part (a): motion diagram and v-t graph | `solution-writing.md` 5, 6 |
| Motion diagram: dots at equal time steps, velocity arrow on each, acceleration drawn separately, chosen directions in a corner | `diagrams.md` 7 |
| Dots stop at 4T/5 and there is no landing circle, so every dot has an arrow and none pierces the ground | `diagrams.md` 3, 7 |
| Part 2 compares two cases: the dropped car is a second dot column and a second dashed line on the same v-t graph, each labeled apart | `solution-writing.md` 5, `diagrams.md` 7 |
| Each plug-in with negative values is preceded by a line giving those values with direction words | `physics-language.md` 4 |
| Solving for a time that starts from rest still opens with the full EQUATION step | `solution-writing.md` 3 |
| Situation figure text renders at 0.94 of body size (11 px in-SVG at 1.25 scale) | `diagrams.md` 2 |
| Absolute-value bars are `<mo>` fences, and numbers are `<mn>` with a separate unit `<mtext>` | `solution-writing.md` 9 |
| `g = 9.80 m/s²` is one MathML equation | `solution-writing.md` 9 |
| v-t graph: numbered scale and units on both axes, clean-number scales | `diagrams.md` 1 |
| Explicit CSS width and height on every figure, render ratio 1.2 to 1.3 | `diagrams.md` 2 |
| Arrowheads from `tools/svgarrow.py`, shaft stops at the head, one marker per role | `diagrams.md` 3 |
| Cliff and ground hatched on the solid side; height marker on the open-air side, label beside its middle | `diagrams.md` 6 |
| Range marker below the ground, set away from what it measures, so it has end lines | `diagrams.md` 6 |
| Subscripts in SVG are tspans; the step back up sits on following text | `diagrams.md` 4 |
| Velocity blue, acceleration green, displacement ink; color is a role | `diagrams.md` 5 |
| Every equation is MathML from `tools/mathml.py`; parenthesized values are `<mrow>` wrapped so exponents render | `solution-writing.md` 9 |
| "Kinematic equations" only; equation sheet lists base equations and no convention | `physics-language.md` 6, 9 |
| Part 2(c) states the expected result ("should reach the ground at the same time") and a check, not "justify" | `physics-language.md` 10 |
| No banned motion words and no em dashes anywhere in the output | `physics-language.md` 1, 13 |
| Generic Name, Date, Period header; no school or teacher text | repository scrub rule |
