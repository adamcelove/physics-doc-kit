---
name: solution-keys
description: Write an answer key or any worked solution for a physics document. Covers key-as-toggle, symbolic-before-numbers, sign conventions as choices, the two required figures, and the derivation rules that replace "by symmetry". Load before writing a key, a worked example, a solution walkthrough, or any calculation a student will read. Also load when adding answers to an existing worksheet.
---

# Writing Solutions

Load these before writing (paths relative to `${CLAUDE_PLUGIN_ROOT}/standards/`): `solution-writing.md` (the full standard, with layout values and the handback checklist), `answer-key-toggle.md`, `diagrams.md`, `physics-language.md`. The checklist below is binding on its own.

## Must-do checklist

1. **The key is a toggle on the worksheet, never a second file.** Answers are `.ans` elements, hidden by default and shown by `body.key`. Add the toggle with `python3 ${CLAUDE_PLUGIN_ROOT}/tools/add-key-toggle.py <file.html>`, or emit it from the builder. `?key` in the URL turns it on. Never create a `*-answer-key.html` sibling.
2. **printfit is for printables, not keys.** Check the blank worksheet state only. Never measure the key state or compress key layout to paginate.
3. **Symbolic before numbers.** Three labeled steps, each on its own line: EQUATION (symbols only), SOLVE FOR THE UNKNOWN (symbols only), PLUG-IN (values with units attached, then the result). Never plug in first and rearrange after. Highlight only the final value.
4. **Units travel with the numbers**, inside the same parentheses, as `<mtext>`: `d = (30 m/s)(0.50 s) = 15 m`.
5. **Sign conventions are chosen, not facts.** Write "I chose down as positive, so v_i = −19.6 m/s (upward)." Restate the choice inside every answer that uses signs. Signed values carry a direction word. Signs are "the same" or "opposite".
6. **Never assert symmetry; derive it.** Banned as arguments: "by symmetry", "the time up equals the time down", "double the time to the top". Derive the return velocity from Δy = 0 (name both roots, rule one out), show equal times from equal Δv at constant a, and reinforce with the equal-area triangles on the v-t graph.
7. **A quadratic gets a calculator path** as well as the formula: expression equals zero, plug in with units, graph it, find each root, then choose among the zeros and say what each survivor is.
8. **Two figures per solution**: a motion diagram (positions, velocity arrows, the acceleration arrow drawn separately, chosen positive direction marked) and a v-t graph with a numbered scale and units on both axes. They go between the stem and part (a), in a block hidden outside `body.key`.
9. **Equations are MathML** (load the `mathml-html` skill).
10. **Spacing:** room after the question before the answer opens, after each answer block, around figures, and between math steps.

## Before handback

Render the key state in a headless browser, screenshot it, and look at it: every label against the arrow it names, the frame, the viewBox edge, and every other label. Arrows stop at the surface they hit. Then confirm the blank state still passes `printfit check <abs-path>`.
