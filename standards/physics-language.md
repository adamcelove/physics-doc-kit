# Physics Language

How to word anything about motion, forces, and vectors: worksheets, labs, quizzes, tests, keys, slides, and written feedback. These rules apply to prose for students and for teachers alike.

## 1. Banned words

Never write **"forward"**, **"backward"**, **"decelerate"**, or **"deceleration"**. There is no context in which they are acceptable.

- *Forward/backward* describe direction relative to a body, not an axis. Direction is a sign on a coordinate axis.
- *Decelerate* fuses "negative acceleration" with "slowing down". They are different things: a negative acceleration speeds an object up when its velocity is already negative.

Wrong: "The cart rolls backward and decelerates."
Right: "The cart has a negative velocity (moving left), and the signs of its velocity and acceleration are opposite, so it is slowing down."

## 2. Describe an acceleration by its signs

Use these four elements, and only these:

1. The sign (direction) of the acceleration.
2. The sign (direction) of the velocity at that moment.
3. Whether those two signs are **the same** or **opposite**.
4. The result, from a closed set: **speeding up**, **slowing down**, **changing direction**, or **constant velocity**.

Right: "The acceleration is negative while the velocity is still positive; the signs are opposite, so the object is slowing down."

## 3. "The same" and "opposite", never "agree" and "oppose"

Students already own "same sign" and "opposite sign" from arithmetic; "agree/oppose" is a second vocabulary for the same idea. Use it in table headers, column entries, model answers, and rubrics.

Wrong: "The signs oppose." Right: "Are the signs the same or opposite?"

## 4. Signed values carry a direction word

Whenever a velocity, acceleration, or displacement is written with a sign, put the direction in words beside it, in prose, tables, and display math alike. A sign alone is too abstract for a student reading a solution.

Right: "v = −41.4 m/s (downward)", "a = +3.2 m/s² (up)", "+11.1 m/s (east)".

Direction words are up/down, left/right, compass points, or "toward/away from" a named landmark (the cup, the wall). Never forward/backward.

## 5. Sign conventions are chosen, and the student chooses

A positive direction is a modeling decision, not a fact about the world. Wording it as fact teaches that down *is* positive.

- **Outside solved work, the student picks.** Prompts, instruction boxes, step lists, table headers, and reference pages never state a convention. They tell the student to choose a positive direction and write it down.
- **Inside answer keys and fully worked examples**, declare the choice in the first person, before any signed value appears, then move on: "I chose up as positive."
- Do not add justification sentences after the declaration ("that is a choice, not a fact", "a different choice flips the signs"). The plain statement is the whole convention.

Wrong (in a key): "Down is positive." "Taking down as positive..." "The direction chosen as positive here..."
Wrong (in a prompt): "Use +x to the right."
Right (in a prompt): "Choose a positive direction for each axis and write it at the top of your work."
Right (in a key): "I chose down as positive, so v_i = −19.6 m/s (upward)."

## 6. Kinematic equations

Call them the **kinematic equations**. Never "SUVAT" or any other label; a second name for the same thing is noise.

## 7. Gravity is F_g

The gravitational force is written **F_g**, and its magnitude near Earth's surface is g = 9.80 m/s², directed downward. Keep the force symbols consistent across prose, free-body diagrams, and interaction diagrams: F_g, F_N, F_f, F_T, F_s.

## 8. Components: opposite and adjacent, never "cos is x"

When a vector is broken into components, never attach cosine to x or sine to y. Problems measure angles from the horizontal, from the vertical, or counterclockwise from +x, and "cos is x" breaks the moment the angle is measured from the vertical.

1. Name the leg that touches the given angle: adjacent = A cos θ, opposite = A sin θ.
2. Then say which leg is horizontal and which is vertical.
3. Then attach signs from the direction words. (Convert a counterclockwise-from-+x angle to a triangle angle first.)

Wrong: "A_x = A cos θ."
Right: "The angle is measured from the vertical, so the vertical leg is adjacent: 12 cos 30° = 10.4 m/s. The horizontal leg is opposite: 12 sin 30° = 6.0 m/s, to the left, so −6.0 m/s."

## 9. Equation sheets list base equations only

A student equation sheet (formula sheet, skills sheet, reference card) lists only definitions, laws, and given constants. Deriving the special case is the skill being assessed.

- **Never list a combined result** for a specific scenario: projectile range, maximum height, or time of flight; free-fall forms of the kinematic equations; N = mg or mg cos θ on an incline; minimum speed at the top of a loop; banked-curve tan θ; orbital speed or period; P = Fv; P = I²R or V²/R.
- **Never list component rules** like A_x = |A| cos θ or v_x = v cos θ. Trig rows are only sin, cos, tan as side ratios and θ = tan⁻¹(opp/adj).
- **Never carry a sign convention.** List g = 9.80 m/s² (magnitude, directed downward) and nothing more: no a = −g, no "take up as positive".

## 10. State what should be true; do not ask students to justify it

Prompts do not ask students to reason "without calculating", "from the description alone", "from the angle alone", or to "justify the vertical component". State the fact and give a concrete check.

Wrong: "From the angle alone, justify why G's vertical component is larger."
Right: "G's vertical component should be nearly three times its horizontal component, because the vector is steep. Check: divide the two sizes from your table."

## 11. Say "diagram", not "motion map"

"Motion map" is not student vocabulary. Ask for a diagram and say what it contains: "a labeled dot above the number line for each second".

## 12. Graph axes

Graph rules (numbered scale and units on both axes, clean-number scales) are in `diagrams.md`.

## 13. No em dashes

No em dashes anywhere in a produced document: prose, headings, captions, SVG labels. They read as machine-written. Use the punctuation the sentence needs (comma, colon, semicolon, parentheses) or rewrite. Heading separators become a colon: "Part 4: the half-court throw". When removing one from existing text, check both sides; a dropped dash often fuses two sentences. Before handback, search the file for the character, `&mdash;`, and `&#8212;`.
