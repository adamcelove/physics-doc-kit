# MathML cheat sheet

## Skeleton

```html
<math display="inline"><mi>a</mi><mo>=</mo>
  <mfrac><mrow><mi mathvariant="normal">&#x394;</mi><mi>v</mi></mrow>
         <mrow><mi mathvariant="normal">&#x394;</mi><mi>t</mi></mrow></mfrac>
</math>
```

No namespace attribute is needed in HTML5. No closing-slash tricks, no `<semantics>`
or `<annotation>` unless you actually need the LaTeX round-trip.

## Element map

| Want | Markup | Helper |
|---|---|---|
| variable | `<mi>v</mi>` | `mi("v")` |
| number | `<mn>9.8</mn>` | `mn("9.8")` |
| operator | `<mo>=</mo>` | `mo("=")` |
| words in math | `<mtext>total</mtext>` | `mtext("total")` |
| subscript `v_f` | `<msub><mi>v</mi><mi>f</mi></msub>` | `sub(mi("v"), mi("f"))` |
| exponent `t²` | `<msup><mi>t</mi><mn>2</mn></msup>` | `sup(mi("t"), mn("2"))` |
| **both**, `v_i²` | `<msubsup><mi>v</mi><mi>i</mi><mn>2</mn></msubsup>` | `subsup(mi("v"), mi("i"), mn("2"))` |
| fraction | `<mfrac><mrow>…</mrow><mrow>…</mrow></mfrac>` | `frac(num, den)` |
| square root | `<msqrt><mrow>…</mrow></msqrt>` | `sqrt(x)` |
| nth root | `<mroot>…</mroot>` | `root(x, n)` |
| vector arrow | `<mover accent="true"><mi>v</mi><mo stretchy="false">&#x2192;</mo></mover>` | `vec(mi("v"))` |
| magnitude | `\|v→\|` with `lspace/rspace=0` bars | `mag(mi("v"))` |
| grouping | `<mrow>…</mrow>` | `row(...)` |
| thin space | `<mspace width="0.15em"/>` | `space()` |

**Never** stack `msup` on `msub` for the same base, `v_i²` is one `msubsup`,
or the exponent sits too far right.

Always `<mrow>` the numerator, denominator, and radicand even when they are a
single token; the helpers do it for you.

## Entities

| Symbol | Entity | Note |
|---|---|---|
| − minus | `&#x2212;` | never `-` (hyphen) |
| × times | `&#xD7;` | scientific notation |
| ⋅ dot | `&#x22C5;` | |
| ∝ proportional | `&#x221D;` | |
| ≈ | `&#x2248;` | |
| Δ | `<mi mathvariant="normal">&#x394;</mi>` | upright, it's an operator prefix |
| θ | `&#x3B8;` | plain `<mi>`, italic is correct |
| π | `&#x3C0;` | |
| μ | `&#x3BC;` | |
| ω | `&#x3C9;` | |
| ° degree | `&#xB0;` | as `<mo>` |
| invisible apply | `&#8289;` | between function name and argument |

Greek *variables* are italic `<mi>`; Greek *operators* (Δ) are upright.

## Negative numbers vs. subtraction

- Binary subtraction: `<mo>&#x2212;</mo>` (`MIN`), gets space on both sides.
- Leading sign on a value: `<mo form="prefix" lspace="0" rspace="0">&#x2212;</mo>`
  (`NEG`), tight, so `−9.8 m/s²` doesn't read as a subtraction.

## Function names

```html
<mi>sin</mi><mo>&#8289;</mo><mspace width="0.12em"/><mi>&#x3B8;</mi>
```
`fn("sin") + TH`. Inverse: `sup(fn-name-as-mi, row(NEG, mn("1")))`.

## Stylesheet

```css
math { font-family:"Latin Modern Math","STIX Two Math","Cambria Math","Times New Roman",serif;
       font-size:11.2pt; line-height:1; }
```
Size MathML ~1.2× the surrounding body text, it reads small at matched size.
For a label-beside-equation grid use the `.eqrow` / `.lbl` pattern in
`${CLAUDE_PLUGIN_ROOT}/tools/mathml.py`.

## Worked physics equations

```python
# v = d / t
M(mi("v"), EQ, frac(mi("d"), mi("t")))

# a = Δv / Δt
M(mi("a"), EQ, frac(DEL + mi("v"), DEL + mi("t")))

# v_f = v_i + a t
M(sub(mi("v"), mi("f")), EQ, sub(mi("v"), mi("i")), PLUS, mi("a"), mi("t"))

# Δx = v_i t + ½ a t²
M(DEL + mi("x"), EQ, sub(mi("v"), mi("i")), mi("t"), PLUS,
  HALF, mi("a"), sup(mi("t"), mn("2")))

# v_f² = v_i² + 2 a Δx
M(subsup(mi("v"), mi("f"), mn("2")), EQ, subsup(mi("v"), mi("i"), mn("2")),
  PLUS, mn("2"), mi("a"), DEL + mi("x"))

# F_net = m a
M(sub(mi("F"), mtext("net")), EQ, mi("m"), mi("a"))

# F_g = G m_1 m_2 / r²
M(sub(mi("F"), mi("g")), EQ,
  frac(mi("G") + sub(mi("m"), mn("1")) + sub(mi("m"), mn("2")),
       sup(mi("r"), mn("2"))))

# p = m v          J = F Δt
M(mi("p"), EQ, mi("m"), mi("v"))
M(mi("J"), EQ, mi("F"), DEL + mi("t"))

# KE = ½ m v²
M(mtext("KE"), EQ, HALF, mi("m"), sup(mi("v"), mn("2")))

# g = 9.80 m/s²  (upright units)
M(mi("g"), EQ, mn("9.80"), space(),
  mtext("m/s") + sup(mtext(""), mn("2")))   # or an <mtext>m/s&#178;</mtext>

# θ = tan⁻¹(opp / adj)
M(TH, EQ, sup(mi("tan"), row(NEG, mn("1"))),
  paren(frac(mi("opp"), mi("adj"))))

# 6.67 × 10⁻¹¹
M(mn("6.67"), TIMES, sup(mn("10"), row(NEG, mn("11"))))
```

Units are `<mtext>` (upright), never `<mi>`, `<mi>m</mi>` italicizes the metre
and reads as a mass variable.

## Checks before handback

1. Open the HTML, no literal `<mfrac>` text on the page, no tofu boxes.
2. Fractions are not clipped by a tight `line-height` or a fixed row height.
3. `printfit check` (blank state only); MathML changes line heights,
   so re-measure the page count.
