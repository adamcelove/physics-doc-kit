# Solution Writing

How every worked solution is structured, in any physics document: answer keys, worked examples, slides, lab exemplars, feedback. The wording rules in `physics-language.md` apply on top of this file; this file governs structure. How much blank space the student gets for the same solution is in `workspace-sizing.md`.

## 1. The key is a toggle on the worksheet, never a second file

Answers live inside the worksheet as hidden elements that a toggle reveals. Never ship a separate `*-answer-key.html`. Mechanics are in `answer-key-toggle.md`.

## 2. Keys are screen documents

A key is read on a screen, often projected. It is not a printable.

- Never run the print check on the key state, and never compress key layout to improve pagination. Page count is not a constraint on a key.
- The blank worksheet is still a printable and must pass the print check.
- Spend vertical space freely: after the question before the answer opens, after each answer block, around figures, and between math steps.

## 3. Symbolic before numbers

Universal. Any calculation that contains values appears first in variables, in three labeled steps, each on its own line:

| Step label | Contains |
|---|---|
| EQUATION | the general relationship, symbols only |
| SOLVE FOR THE UNKNOWN | the algebraic rearrangement, still symbols only |
| PLUG-IN | values **with their units** entered into the solved form, then the result |

- Never substitute into the general equation and rearrange afterward. The algebra is the transferable skill, and it is only visible before the numbers land.
- If the equation already solves for the target, say so and skip step 2. Do not invent a rearrangement.
- Quote the solved symbolic form in the prose that follows; it usually explains the answer. Example: v = √(2aΔy) is why half the drop height does not give half the landing speed.
- Highlight only the final plugged-in value.

**Every value carries its unit in the plug-in step**, inside the same parentheses, so a student can check the line by cancelling units before trusting the arithmetic. A squared value carries the squared unit.

Right: d = (30 m/s)(0.50 s) = 15 m
Wrong: d = (30)(0.50) = 15 m

Older keys label the third step SUBSTITUTE; it is the same step.

## 4. Sign conventions in solutions

Declare the positive direction in the first person, once per problem before any signed value appears, and restate it inside each answer that uses it, because a reader lands on one answer, not the whole page. Every signed value carries a direction word. The full rule, including what prompts may and may not say, is in `physics-language.md` sections 4 and 5.

Right: "I chose down as positive, so v_i = −19.6 m/s (upward)."

## 5. Two figures per solution

Every worked motion solution gets both, including descriptive answers with no calculation. If an answer reasons about signs, the figures make that reasoning visible.

1. A **motion diagram**: positions, velocity arrows, the acceleration arrow drawn separately, and the chosen positive direction marked in a corner.
2. A **velocity-time graph** with a numbered scale and units on both axes.

When two cases are compared, draw both on one v-t graph (same slope, different intercepts is usually the point) and label each line at its midpoint. Drawing rules for both figures are in `diagrams.md`.

## 6. Figures come before part (a)

The figure block sits between the stem and part (a), the first thing inside the problem. On a multi-part problem the figures describe the whole situation, so they must be readable while (a) is worked, not found after (c). On a single-answer item, the figures go immediately before the answer.

```html
<p class="stem">...the situation...</p>
<div class="figs">...motion diagram...v-t graph...</div>   <!-- here -->
<ul class="parts"><li><b>(a)</b> ...
```

The figure block is hidden outside key mode, so placing it here never changes the blank printable's pagination.

## 7. Never assert symmetry: derive it

Banned as arguments: "by symmetry", "the time up equals the time down", "the total time is double the time to the top". They state the result instead of showing it, and they hide the one move students need: choosing between two roots on physical grounds.

**Move 1: the return velocity, from the equation.** Over an interval that ends at the starting height, Δy = 0:

    v_f² = v_i² + 2aΔy, with Δy = 0  →  v_f² = v_i²  →  v_f = ±v_i

Name both roots and rule one out physically: v_f = +v_i would mean the object never turned around. The remaining root, v_f = −v_i, is the answer.

**Move 2: the equal times, from the velocity change.**

    Δv (to the turning point) = 0 − v_i = −v_i
    Δv (back to the start)    = v_f − 0 = −v_i

Same Δv, same constant a, and t = Δv/a depends on nothing else, so the times are equal. Compute the total as their sum.

**Graph reinforcement.** The v-t line crosses zero at the turning point, cutting the motion into two triangles whose areas are the two displacements. Returning to the start makes the areas equal; equal area with equal height |v_i| forces equal base, and each base is a time. Shade both triangles and label them "equal area".

The same two moves give the velocity at any level the object passes twice.

## 8. A quadratic gets a calculator path too

Any solution whose algebra lands on a quadratic in time carries a second route after the symbolic one, not instead of it:

1. Write it as "expression = 0", every term on one side.
2. Plug in with units, so the coefficients are physical: 0 = (4.9 m/s²)t² − (24.5 m/s)t + (19.6 m).
3. Enter it in the graphing calculator as y1 with x standing for t, and say that the calculator carries no units: x is a number of seconds because step 2 said so.
4. Set a window that shows both crossings, starting at x = 0.
5. Find each root with the calculator's root (zero) tool.
6. Choose the roots the situation asks for. A zero is a candidate, not an answer: reject negative times, then say what each surviving root is. That is the physics the calculator cannot do.

Show the calculator screens as a figure. This is a procedure figure, so it stays inline with the step it illustrates; the before-part-(a) rule covers only the situation figures.

## 9. Equations are MathML

Write every equation as native MathML: no math libraries from a CDN, one semantic element per token, U+2212 for minus, units in `<mtext>`.

Known trap: a helper that returns a parenthesized expression without an `<mrow>` wrapper gives `msup`, `msub`, or `mfrac` the wrong child count, and the exponent is silently dropped: (−19.6)² renders as (−19.6)2. Check that exponents on parenthesized quantities actually render raised.

## 10. Layout values that work

```css
body.key .ans{margin:12px 0 20px}        /* after question, after answer */
body.key .parts li{margin:14px 0}
.ans .calc{margin:10px 0;padding:2px 0 2px 10px;border-left:2px solid #cfe3d7;
           line-height:1.75}             /* one math step, with room */
.ans .calc+.calc{margin-top:12px}
.ans .steplab{font-size:8pt;text-transform:uppercase;color:#6b8f7d}
.ans .fill{background:#dcefe3;padding:1px 6px;border-radius:3px}
```

## 11. Checklist before handback

- [ ] Key is a toggle on the worksheet file; no separate key file
- [ ] Every calculation: equation, solve, plug-in, with units on every plugged-in value
- [ ] Positive direction declared as a first-person choice in every answer that uses signs
- [ ] Signed values carry a direction word; "same/opposite", never "agree/oppose"
- [ ] Motion diagram and v-t graph on every solution; both graph axes scaled and with units
- [ ] Figure block before part (a) or before the answer, never at the end
- [ ] Quadratic solutions carry the calculator path and the root choice
- [ ] No appeal to symmetry or doubling; return velocity and equal times derived
- [ ] Key rendered and inspected for label collisions and overflow (`diagrams.md` section 8)
- [ ] Equations are MathML; exponents on parenthesized quantities actually raised
- [ ] Print check passes on the blank state; key state not checked
