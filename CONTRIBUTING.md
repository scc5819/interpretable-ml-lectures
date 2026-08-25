# Contributing

This is our course's shared repository — each seminar can become a module, and
anyone can improve any module. This page is the practical how-to; the CI does
the nitpicking automatically, so nobody has to.

## Your first contribution

1. **Fork** the repository and clone your fork.
2. **Set up the environment** (Python 3.14 — the committed numbers were produced on it):

   ```bash
   python3.14 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   jupyter notebook
   ```

   To reproduce the committed outputs exactly, `pip install --require-hashes
   -r requirements.lock` installs the full locked stack instead.

3. **Run a walkthrough notebook** end to end (e.g. `modules/14-lime/notebooks/lime_walkthrough.ipynb`) to see the format working.
4. **Branch, change, open a pull request.** CI runs the notebooks and checks links and formatting on every PR — if something is off, the robot says exactly what, before anyone else even looks.

One heads-up: the first cell of every notebook is `%pip install -q …` with no
version pins. That is on purpose — it is what makes the Colab badge work, and
in a prepared venv it is a no-op. Leave it as is (no `-U`, no versions).

## The evidence bar

The one idea that makes this material worth publishing — everything in it can
be checked, not just believed:

1. **A number stated in prose is printed by a committed notebook cell in the
   same module**, so any reader can re-run it.
2. **Numbers carry their conditioning** — sample size, seed, span — so they
   can be compared honestly.
3. **When a claim turns out wrong, the text is corrected and a note of the
   old value stays.** Corrections are part of the material, not something to
   hide — the LIME module keeps several of its own, and they are some of its
   best teaching moments.

Two practical notes: quotes from the literature are verbatim with section
pointers, and we cite and link Molnar's book rather than pasting its figures
(the book is CC BY-NC-SA; our content is CC BY-SA — compatible only at a
distance).

## Notebook conventions

- Two notebooks per module: `<slug>_walkthrough.ipynb` (the lecture) and
  `<slug>_internals.ipynb` (the companion that checks the method against its
  own library).
- `RANDOM_STATE = 42`; data splits stated explicitly.
- Figures go to `figures_generated/` (git-ignored); the committed copies live
  in `modules/NN-slug/figures/` and are promoted by hand, so a committed
  figure never changes silently.
- Commit notebooks **with outputs**, after *Restart & Run All* in a fresh
  kernel — that is what makes the numbers checkable.
- Keep outputs deterministic: no timestamps, no `%%time`, no progress bars.

(CI verifies all of this automatically — the list is here so the robot's
messages make sense, not so anyone memorizes it.)

## Adding a new module

Claim your chapter first via the [new-module issue form](https://github.com/scc5819/interpretable-ml-lectures/issues/new/choose),
so two people don't build the same one. Module numbers are Molnar's chapter
numbers. Then start from [`modules/_template/`](modules/_template/):

```
modules/NN-slug/
├── README.md
├── figures/
├── lecture/
│   └── outline.md
└── notebooks/
    ├── <slug>_walkthrough.ipynb
    └── <slug>_internals.ipynb
```

When it lands, run `python3 tools/render_board.py` and commit the README
change — your row in the module table flips to *available* by itself.

Two things that help the series read as one continuous case: keeping the
shared setup where it fits (Breast Cancer Wisconsin dataset,
`RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=42)`,
test patient #67 — chapters 27–31 will naturally need their own), and noting
in the README when a module overrides a package default, so readers comparing
with other tutorials know why outputs differ.

A note on dependencies: the pins in `requirements.txt` are what make the
committed numbers reproducible, so version bumps travel together with a full
re-run of the notebooks (Dependabot only watches GitHub Actions here, where a
bump changes no printed number).

Delivered slide decks are historical records — they keep their presenter's
name and are not retro-edited; the living, editable form of a lecture is its
`lecture/outline.md`.

## Contact

Questions, suggestions, or anything you'd rather raise privately:
[@wbendinelli](https://github.com/wbendinelli) — <william.bendinelli@alumni.usp.br> —
or the course professor. Commit style follows the existing history
(`docs(14-lime): …`, `fix(14-lime): …`); look at `git log` and copy the shape.

## Licensing of contributions

By opening a pull request you agree that your prose, figures and outlines are
published under [CC BY-SA 4.0](LICENSE-CC-BY-SA-4.0.md) and your code under
[MIT](LICENSE) — always with attribution to you. Authoring a module earns an
entry in [`CITATION.cff`](CITATION.cff)'s author list; every contribution is
credited by the commit history either way. There is no CLA.
