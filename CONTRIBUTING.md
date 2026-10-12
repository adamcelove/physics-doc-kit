# Contributing

The rules live in `standards/`. A change to what a worksheet or key must look like is a change to a standard first; skills and hooks only restate the standards tersely.

Before opening a pull request:

1. `uv run python scripts/scrub-check.py` passes (no private names, paths, or student data).
2. `uv run pytest -q` passes.
3. Any example you add or change passes `printfit check` on the blank state with `verdict: pass`. Answer keys are exempt.
4. No em dashes, and none of the banned motion words defined in `standards/physics-language.md`, outside the files that define the ban.
5. Examples are built by their `build.py`; edit the builder, never the generated HTML.

Standards are CC BY 4.0; code is MIT. By contributing you agree to those terms.
