# Contributing

This repository is a set of lecture materials built on one commitment: every claim is measured rather than asserted (see [How these materials are built](README.md#how-these-materials-are-built)). Contributing here means holding your change to that same bar — and holding the existing material to it, which is the contribution we want most.

## Your first contribution

1. **Fork** the repository and clone your fork.
2. **Set up the environment** (Python 3.14 — the committed numbers were produced on it):

   ```bash
   python3.14 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   jupyter notebook
   ```

   To reproduce the committed outputs exactly, install from the fully resolved
   lockfile instead — it pins every transitive dependency with hashes:

   ```bash
   pip install --require-hashes -r requirements.lock
   ```

3. **Run a walkthrough notebook** end to end (e.g. `modules/14-lime/notebooks/lime_walkthrough.ipynb`) and check a printed number against the module's README. That round trip — prose claim to notebook cell — is the standard everything here is held to.
4. **Pick something**: an issue labeled `good first issue`, an open chapter from the [module table](README.md#modules), or any claim you think you can falsify.
5. **Branch** (`fix/…`, `docs/…`, or `module/15-counterfactuals`), make the change, and open a pull request — the template will ask where your numbers come from.

One thing not to "fix" along the way: the first cell of every notebook is `%pip install -q …` with **no version pins**. That is deliberate — it is there for Colab, and in a prepared venv it is a no-op because pip treats already-satisfied unpinned requirements as satisfied, so the pins in `requirements.txt` hold. Never add `-U` or inline versions to that cell. The rationale for the pins themselves is in the header of [`requirements.txt`](requirements.txt).

## What we're looking for

In priority order:

1. **Falsifications.** A measurement showing that a claim in this repository is wrong. This is the most valuable kind of PR, and the repository already carries the precedent: the LIME module's R²-versus-confidence finding was withdrawn after replication failed on other models and datasets, and the record of that failure is kept in the module rather than deleted. Do that to us again.
2. **Replications.** The same measurement on other datasets and model classes (the LIME module's §11b kernel-deletion sweep across four datasets and three model classes is the pattern to imitate).
3. **Corrections.** Broken links, misquotes, citation errors, arithmetic.
4. **New modules.** One Molnar chapter each — see the [module table](README.md#modules) and [Adding a new module](#adding-a-new-module).
5. **Clarity edits** to prose and lecture outlines.

**Out of scope** (so nobody wastes a weekend):

- Restyling figures without a measured reason.
- Adding a method or a claim with no measurement behind it.
- **Drive-by dependency additions or version bumps.** The pins in `requirements.txt` (resolved with hashes in `requirements.lock`) are what make the committed numbers reproducible; a bump is a content change that requires re-running every notebook, regenerating every figure, and re-checking every number quoted in prose. Dependabot is disabled for Python packages on purpose, and version-bump PRs that don't do that work will be closed. The one deliberate exception is GitHub Actions: an action bump changes no printed number, so `.github/dependabot.yml` watches the `github-actions` ecosystem only. The Python baseline *does* move — deliberately: CI runs a weekly non-blocking canary of the walkthroughs on the newest Python and unpinned latest packages, and when the maintainers upgrade the baseline (typically once per course offering, or when the canary shows real breakage), it happens as one PR that updates the pins, regenerates `requirements.lock`, *and* everything downstream of them.
- Translations — open an issue first; a translated fork is usually the better answer.

## The evidence bar

Every PR that touches a claim is reviewed against these six rules:

1. **Every quantitative claim in prose is printed by a committed notebook cell in the same module.** The PR description must name the notebook and the section that prints each changed number.
2. **Numbers come from a run against the pinned `requirements.txt` on Python 3.14.** A number produced in a different environment is a different number.
3. **Report the conditioning.** Sample size, seed, and any span, threshold or grid choice — and what happens when it changes. An unconditioned number reads as an assertion.
4. **Negative and withdrawn results are kept, not deleted.** A PR that falsifies a claim rewrites the claim *and* keeps the record of what failed and why — that record is part of the material.
5. **Quotes from the literature are verbatim, with section-level pointers** (e.g. §3.2.3), not paraphrase presented as quotation.
6. **Do not paste figures or extended passages from Molnar's book.** The book is CC BY-NC-SA; this repository's content is CC BY-SA, and the two are compatible only as long as we cite and link rather than reproduce. All committed figures must be generated by the notebooks in this repository.

## Notebook conventions

- Two notebooks per module: `<slug>_walkthrough.ipynb` (the lecture) and `<slug>_internals.ipynb` (the technical companion that validates the library against its own source code and measures the method's behavior independently of its documentation).
- `RANDOM_STATE = 42` throughout; data splits stated explicitly in the notebook.
- **Figures.** Notebooks write to `figures_generated/` (relative to the notebook directory, git-ignored). Canonical figures are committed by hand into `modules/NN-slug/figures/`, so a committed figure never changes silently. A PR that changes a committed figure must say which cell regenerated it and why the picture moved.
- **Commit notebooks with outputs** — that is how the numbers are checkable. Run *Restart & Run All* in a fresh kernel first, so execution counts run 1..N.
- Keep outputs deterministic: no wall-clock timestamps, no `%%time`, no progress bars that bake elapsed time into stored output.
- `jupytext` (in the tooling block of `requirements.txt`) is handy for diffing notebooks as text; pairing is optional and no `.py` sources are tracked.
- Overriding a package default (as the LIME module does with `discretize_continuous=False`) requires a matching "A note on configuration" section in the module README, so readers comparing against other tutorials know why the outputs differ.

## Adding a new module

Claim a chapter **before** writing it, via the [new-module issue form](https://github.com/scc5819/interpretable-ml-lectures/issues/new/choose) — scope and numbering get agreed there, and the module table gets your name on the row. Module numbers are Molnar's chapter numbers.

Start from [`modules/_template/`](modules/_template/):

```
modules/NN-slug/
├── README.md                  # section order in the template
├── figures/                   # committed canonical figures, notebook-generated
│   └── .gitkeep               # placeholder — delete once real figures land
├── lecture/
│   └── outline.md             # required — the editable form of the lecture
└── notebooks/
    ├── README.md              # conventions crib sheet — delete once the notebooks exist
    ├── <slug>_walkthrough.ipynb
    └── <slug>_internals.ipynb
```

When the module lands, run `python3 tools/render_board.py` and commit the README change — the module table is **generated** from [`schedule.toml`](schedule.toml) plus the `modules/` tree, and your row flips to *available* automatically. Edit `schedule.toml` (dates, titles, presenters), never the table itself; a weekly CI check files an issue when the board drifts.

Rules that keep the series reading as one case:

- **Keep the shared case.** Same dataset (Breast Cancer Wisconsin Diagnostic, as shipped with scikit-learn), same model (`RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=42)`), same split, same test patient #67. Deviate only with a measured reason, stated in the README. (Modules on chapters 27–31, neural network interpretation, will necessarily need their own case — say what it is and why.)
- **`lecture/outline.md` is required; a slide deck is optional.** The outline is the artifact the community can edit. Delivered decks are historical records of a talk given by a person on a date — they carry their presenter's name and are not retro-edited.
- The module README follows the template's section order (the "What the literature proposes to do about it" section is optional — include it when the module's findings have a literature of proposed fixes to map), ending with a References list where each entry says in a parenthetical what it is being cited *for*.

## Pull request workflow

Fork → branch → commit → PR → CI → review.

- **Commit style** follows the existing history: `docs(14-lime): …`, `fix(14-lime): …` — type plus the module slug as scope. A falsification is a `fix`.
- **Branches**: `fix/…`, `docs/…`, `module/NN-slug`.
- CI runs a link check and executes the walkthrough notebooks against the pinned environment; the internals notebooks run when a PR touches them. A PR that leaves the working tree dirty after notebook execution fails CI.

## Review expectations

Review checks the [evidence bar](#the-evidence-bar) above, point by point. Reviewers may ask for a re-run with different conditioning (a different span, seed, or sample size) before merging. Expect turnaround in days, not hours — this is a course repository maintained by people with coursework. Falsification PRs are looked at first.

## Maintainers

| Maintainer | Scope |
|---|---|
| [@wbendinelli](https://github.com/wbendinelli) | repository, module 14 |

Mirrored in [`.github/CODEOWNERS`](.github/CODEOWNERS). Authoring a module makes you the natural maintainer of it; the table grows with the modules.

## Licensing of contributions

By opening a pull request you agree that your prose, figures and outlines are published under [CC BY-SA 4.0](LICENSE-CC-BY-SA-4.0.md) and your code under [MIT](LICENSE). There is no CLA. Authoring a whole module earns an entry in [`CITATION.cff`](CITATION.cff)'s author list; every other contribution is credited by the commit history and the contributor graph.

Conduct in issues, PRs and reviews is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
