# Diagrams and Graphs

Rules for every figure in a worksheet, quiz, test, lab, or key: graphs, grids, motion diagrams, situation sketches, vector figures, free-body and interaction diagrams. Which figures a solution needs is in `solution-writing.md`.

## 1. Graph axes: numbered scale and units, always

- **Every graph gets a numbered scale and units on both axes.** No exceptions, including blank grids students will plot on or sketch on.
- The **only** exception is a task whose stated skill *is* labeling axes or choosing a scale. Then the omission is deliberate and the instructions say so.
- When a graph is read quantitatively, choose the scale so slopes, areas, and intercepts come out as clean numbers, and verify by computing them before shipping.

Wrong: a v-t grid with "v" and "t" and no numbers. Right: "v (m/s)" with ticks at −10, −5, 0, 5, 10, and "t (s)" with ticks at 0 to 4.

## 2. Figure sizing (SVG in HTML)

- Every figure gets an **explicit CSS width and height**. Never `height:auto` or a bare `width:100%`; `width`/`height` attributes alone are not enough for print checks that read declared CSS width.
- Keep rendered width ÷ viewBox width between about 1.2 and 1.6, so in-figure text lands near 0.8 of body size (for example, a 170-unit viewBox rendered at 220px).
- When a figure is shrunk, scale its in-SVG font size up so nothing drops below 7px rendered. Label text under 12px in the source drawing is a warning sign.
- Shaded cells or bands that must print need `print-color-adjust: exact` in a print media rule.

## 3. Arrows: the shaft stops at the head

A vector's line must end at the base of its arrowhead, so nothing of the shaft shows past, beside, or behind the head. Dashed component vectors are the usual offender. Zoom-check the tips of thick or dashed vectors before handback.

- **TikZ:** draw shaft and tip as **one path** (`\draw[vel] (A) -- (B);`). TikZ then shortens the shaft for the head. Never draw a line to the tip and add a separate head.
- **Raw SVG:** do not hand-roll a different marker per figure; use one helper that gets both of these right:
  1. *Symmetric head.* Base from (0,0) to (0,2h), tip at (len,h), `refY = h`. If the tip and base midpoint disagree, one barb comes out longer.
  2. *Shaft shortened.* A head is narrowest at its tip, so a line ending near the tip pokes out as a nub. Set `refX = 0` (the head's base on the line's end) and shorten the shaft by exactly the head length, so the point still lands on the true endpoint and the figure stays measurable.
- Any stroke that carries a head gets `stroke-linecap: butt`; a round cap adds a blob past the point.
- Arrows stop at the surface they hit. A velocity arrow never pierces the ground line.

## 4. Labels and subscripts

- Labels sit beside what they name, touching nothing, at the same offset for matching points. **No leader lines.** Do not force two labels onto one shared baseline.
- Anchor labels away from what they annotate: `text-anchor="end"` to the left of a line, `middle` above it.
- Check every label against the arrow it names, the frame edge, the viewBox boundary, and every other label.
- Variables italic, units upright.
- **SVG subscripts** are a `<tspan>` shifted down, never a literal `v_f`. When a label has more than one subscript, the step back up to the baseline must sit on the **text that follows**, not on an empty tspan, which Chrome ignores (every later symbol then sits low):

```html
<!-- Right -->
(x<tspan dy="3" font-size=".72em">i</tspan><tspan dy="-3">, y</tspan><tspan dy="3" font-size=".72em">i</tspan><tspan dy="-3">)</tspan>
<!-- Wrong: the empty tspan is ignored, so y sits below x -->
(x<tspan dy="3" font-size=".72em">i</tspan><tspan dy="-3"></tspan>, y...
```

The error only shows in the rendered image, so render at 200 dpi or more and zoom in on every subscripted label.

## 5. Colors are roles

| Role | Color |
|---|---|
| Velocity | `#1F5FBF` blue |
| Force | `#BE4C02` orange |
| Acceleration | `#2E8B57` green |
| Displacement / position | `#222222` ink |
| x component | `#11AC33` bright green, thick dashed |
| y component | `#A60156` crimson, thick dashed |

Every pair is perceptually distinct, x and y separate in grayscale print, all stay distinct under common color-vision deficiencies, and all have at least 3:1 contrast on white. A component is always a different color from its full vector. Color is never decoration.

## 6. Drawing rules

- **Before drawing a new kind of figure,** list every marker, vector, and label with its start and end points. Then draw it.
- **Keep numbers in one place.** Generate the figure from the same variables as the problem text so they cannot disagree.
- **Components on an axis** are drawn directly on the axis line in the thick dashed component style, so they read over the thin axis.
- **Distance and height markers** start exactly at the reference point the problem names and contrast with the terrain behind them. A marker drawn right beside the measured feature has arrowheads at both ends, no end bars, on the open-air side (never on hatching). Use end bars only when the marker is set away from what it measures. Label beside the middle.
- **A distance an object travels** starts at the object's leading edge, not at the end of the track.
- **Surfaces:** ground, walls, cliffs, and banks are hatched on the solid side. Under a ramp only the ground is hatched; the slope is a plain outline.
- **Angles:** an arc with the label inside the wedge; for angles under about 25° use a larger radius so the label fits. An angle measured from a direction not already drawn (the horizontal at a launch point) gets a thin dotted reference line extending past the arc.
- **Words in figures:** never forward, backward, or decelerate (see `physics-language.md`).

## 7. Motion diagrams

- One dot per equal time interval.
- **Every dot gets a velocity arrow, including the last.** A zero velocity is labeled v = 0 instead. Each arrow starts at the dot's edge and stops short of the next dot.
- The acceleration arrow is drawn separately, above or below the diagram, never off to the side.
- The chosen positive direction is marked in a corner (in keys; students mark their own).
- A motion that reverses (a ball tossed up) uses two columns close together (about 1 cm apart), the up column on the left.

## 8. Interaction diagrams

- Every object, including the ones inside the system, gets a **solid outline**.
- The **dashed system boundary** goes around all system objects, so lines for external forces visibly cut through it and external versus internal reads at a glance.
- Interaction labels use the **same force symbols as the free-body diagram** (F_g, F_N, F_f, F_T, F_s), never words like "gravitational".
- **One line per force.** Separate forces between the same two objects get separate lines (table to cup: one F_N line and one F_f line), drawn as curves that bow apart, land at different points on each object, and sit at least 8px apart.

## 9. Render and look

Every figure is rendered and inspected before handback, in the state a reader sees it (blank state for the printable, key state for key figures). A headless browser screenshot is enough:

```
chrome --headless=new --disable-gpu --hide-scrollbars \
  --window-size=900,6200 --screenshot=out.png page.html
```

Check labels (section 4), arrow tips (section 3), and that nothing is clipped at the viewBox edge.
