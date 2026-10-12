# Work Space Sizing

How much blank space follows each question on any student document where work is shown: tests, quizzes, worksheets, homework. What a calculation looks like (which is what this standard counts) is in `solution-writing.md`.

## 1. Blank space, never ruled lines

Every response area is **blank, unruled space**. Never draw answer lines.

Why: ruled lines force equations onto a baseline, leave no room for a scratch sketch beside the algebra, and signal "write one sentence" where multi-step work is wanted. The size of the space itself tells the student how much is being asked.

Only exceptions: the Name field, an inline fill-in blank inside a sentence, and a small bordered box for a single final answer.

## 2. Size by lines of work

Space is sized to the work a strong student writes, never to what fits on the page.

- A **line** is one written row of work: an equation, a symbolic rearrangement, a substitution, a result, or one sentence of reasoning.
- A **calculation** solves for one unknown from one equation: 4 lines (equation, solve in symbols, plug in with units, answer).

**Height = 0.30 in × lines + 0.25 in**, rounded up to the next 0.1 in.

| Kind of response | Lines | Height |
|---|---|---|
| One value (reading, table cell, final answer) | none: inline blank or answer box | none |
| Short explanation, 1 to 2 sentences | 2 | 0.9 in |
| Claim plus reasoning, 3 to 4 sentences | 4 | 1.5 in |
| One calculation | 4 | 1.5 in |
| Argument made with an equation ("show why the landing speed equals the launch speed") | 5 | 1.8 in |
| Two calculations (reaction distance, then braking distance) | 8 | 2.7 in |
| Quadratic in time; or a vector as magnitude, angle, and direction in words | 9 | 3.0 in |
| Each further calculation in the same part | +4 | +1.2 in |

Count lines by writing the key solution first. The key's line count is the part's line count.

## 3. Drawing comes first, in its own area

- **A problem that needs the situation visualized starts with a drawing step.** Part (a) asks for the sketch: the motion diagram, or the setup sketch with the origin marked, the positive directions chosen, and the knowns listed in two columns (x and y) when there are two dimensions.
- **Every forces problem starts with a free-body diagram.** Part (a) asks the student to draw the FBD, mark the directions they chose as positive, write the sum of forces in x and in y, and set each equal to *ma*. Space for (a): a 2.0 in tall row, FBD region (3.2 in wide) on the left, the two force-sum equations on the right.
- A drawing region is **2.0 in tall** and at least 2.5 in wide. Put it beside the stem or beside a calculation when the width allows; a sketch next to the algebra is the point of unruled space.
- A graph the student draws gets a **provided grid**, at least 2.2 in tall, with a numbered scale and units on both axes. The grid is not work space: a calculation made from the graph gets its own space by section 2.

## 4. One space per part

Size (a), (b), and (c) separately. Never pool a problem's parts into one shared block.

## 5. Floors and fill

- No written response gets less than **0.8 in**. Anything smaller is an inline blank.
- After sizing, give each page's leftover room to its spaces, calculations first, until the work space reaches the bottom margin.
- **Margin allowance.** The last part on a page may be printed up to 0.5 in shorter than its standard size, ending at the bottom margin; students write into the margin, so their real room is unchanged. Only the last part on a page gets this, never two parts on one page.
- If a page overflows, cut intro prose or add a page (print double-sided). **Never shrink work space below this standard to make a page fit.** A passing print check is not a reason to shrink.

Why: every correction made to real materials asked for more space, never less. Sheets that were squeezed until the print check passed gave the same four-part problem a third of the space it got elsewhere. Sizing by line count removes that drift.

## 6. Tests

- **An assessment-style problem is one stem with three subquestions, (a) to (c), on one page.** That is also the most any test page holds. A subquestion is one lettered item with its own work space.
- **Subquestions are big.** Each covers a wider idea and needs several steps, not one pre-digested step. The standard subquestion is two calculations (8 lines, 2.7 in); the last one on the page is 2.2 in under the margin allowance. Three of those plus the stem fill one letter page.

  Wrong: "(i) Find the normal force. (ii) Find the friction force. (iii) Find the acceleration."
  Right: "Find the acceleration of the crate."
- **Forces problems:** (a) is the FBD plus the force sums (section 3); (b) and (c) are 8-line subquestions.

## 7. Worksheets, quizzes, homework

Same scale, same formula, same look, so a test page is familiar when students meet it. A worksheet may break a problem into more, smaller parts than a test (scaffolding is the worksheet's job), but each part is still sized by section 2. No per-page part limit.

## 8. Wording

- Do not label a space "work space", and do not print a time allowance.
- Every explanation prompt states its expected length: "in 1 to 2 sentences."

## 9. Mechanics

A space is a block element with an explicit inline height, so the line count stays traceable in the builder. Record the count in a comment:

```html
<span class="sp" style="height:2.7in"></span>
```
```python
sp(ws(8))  # two calcs
```

Page-break mechanics (keeping a question together, sections at page top) are in `worksheet-anatomy.md`.
