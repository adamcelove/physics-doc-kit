# Example: horizontal launch worksheet

A two-problem worksheet built to the standards in `standards/`, shipped **with its full answer key**.

- Open `worksheet.html` in a browser. Press the **Answer key** button (top right) to reveal the worked solutions, or open `worksheet.html?key` to load with the key already on.
- Printing prints the **blank** worksheet. The key and its figures are hidden in print.
- `build.py` generates the file: `python3 build.py`. Edit the builder, never the HTML.

| File | What it is |
|---|---|
| `worksheet.html` | the worksheet and its answer key in one file |
| `build.py` | the builder (uses `tools/mathml.py`, `tools/svgarrow.py`, `tools/key-toggle`) |
| `printfit-report.txt` | print check of the blank state: `verdict: pass`, 3 pages |
| `preview.png` | page 1 of the blank printable |
| `key-preview.png` | Part 1 in key state: figures, then each worked answer |
| `WALKTHROUGH.md` | each design decision and the standards rule behind it |

The print check runs on the blank state only; keys are screen documents (see `standards/solution-writing.md`).
