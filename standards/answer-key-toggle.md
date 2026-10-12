# Answer Key Toggle

Every HTML document with answers (worksheet, quiz, test, key) ships with an **Answer key** toggle, so the key is a state of the document rather than a second file.

## 1. How it works

- Answers are `.ans` elements inside the worksheet, hidden by default.
- A single fixed, screen-only button (top right, hidden in print) toggles `key` on `<body>`. `body.key` reveals every `.ans`.
- `?key` in the URL turns key mode on at load, so a key link is the worksheet's URL with `?key` appended.
- The button hides itself when the document has no `.ans` elements.
- Key mode also hides the blank work space, so the key reads as a document instead of a page full of gaps:

```css
.ans{display:none}
body.key .ans{display:block}
body.key .sp{display:none}
@media print{#bar{display:none}}
```

Never ship a separate `*-answer-key.html` file.

## 2. Answer text is one point larger

Key text is set one point larger than the question text it answers (11pt questions, 12pt answers), because keys are read on screen and often projected. Any sizes nested inside `.ans` (step labels, calculation lines, inline table answers) shift by the same amount, so the key keeps its internal hierarchy. The blank printable is unaffected because `.ans` is hidden there.

## 3. Keys are screen-only and never print-checked

- Run the print check on the **blank state only**. Never run it on key mode, never inject `<body class="key">` into a scratch copy to measure it, and never compress key layout to improve pagination.
- Report the page and fill table for the blank printable only.
- Print output of the blank document must be unchanged by adding the toggle. When in doubt, compare page counts before and after with a headless-browser PDF.

## 4. How to add it

Write the document plain, then run the toggle script on it (idempotent; a force flag refreshes an older copy to the current snippet). In a generated document, emit the toggle from the builder or template instead, or the next build will remove it.

The toggle is all that ships by default. Do not add click-to-type editing, save-to-file, or table row tools unless asked.

## 5. When not to add it

- **Embeds into a platform that strips scripts and style blocks** (many learning-management systems). Build those as a separate inline-styled version with no toggle.
- **claude.ai Artifacts**, which have their own sandbox.
- **Script-regenerated outputs**: apply the toggle to the template the script emits, not to the output.
