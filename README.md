# Interpretable ML — Lecture Materials

[![CI](https://github.com/scc5819/interpretable-ml-lectures/actions/workflows/ci.yml/badge.svg)](https://github.com/scc5819/interpretable-ml-lectures/actions/workflows/ci.yml)
[![canary](https://github.com/scc5819/interpretable-ml-lectures/actions/workflows/canary.yml/badge.svg)](https://github.com/scc5819/interpretable-ml-lectures/actions/workflows/canary.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scc5819/interpretable-ml-lectures/main)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY-SA 4.0](https://img.shields.io/badge/content-CC%20BY--SA%204.0-blue.svg)](LICENSE-CC-BY-SA-4.0.md)

Lecture materials on machine learning interpretability for **SCC5819 — Topics in Artificial Intelligence**, a graduate course at the Institute of Mathematics and Computer Sciences, University of São Paulo (ICMC-USP), Brazil, taught by Prof. Dr. André Carlos Ponce de Leon Ferreira de Carvalho. The materials follow the structure and terminology of the course's reference book, Christoph Molnar's [*Interpretable Machine Learning*](https://christophm.github.io/interpretable-ml-book/), covering it one lecture module per chapter from chapter 12 onward.

Each module covers one method, on real data, with every claim measured rather than asserted.

The repository is built by the course's students: corrections, replications and new modules arrive as pull requests — [CONTRIBUTING.md](CONTRIBUTING.md) has the step-by-step.

## Modules

One module per chapter of Molnar's book, from chapter 12 on, written by the course community: each seminar's presenter is the natural author of that chapter's module. That is an invitation, not an obligation — *awaited* describes the state of the material, and the [first-contribution guide](CONTRIBUTING.md#your-first-contribution) is the on-ramp for authors who haven't set foot on GitHub yet. See [Adding a new module](CONTRIBUTING.md#adding-a-new-module) for the template.

<!-- board:begin -->
<!-- Generated — edit schedule.toml and run:  python3 tools/render_board.py
     Do not edit this block by hand. -->
**1 of 21 modules available** · 4 of 22 seminars presented · next session 2026-08-31 (ch. 17, 18).

| Ch. | Method | Presenter | Seminar | Module |
|---|---|---|---|---|
| 12 | Ceteris Paribus Plots | Ana Julia Gonzalez Tendulini | 2026-08-17 — presented | awaited |
| 13 | Individual Conditional Expectation (ICE) | Fabiano Berardo de Sousa | 2026-08-17 — presented | awaited |
| 14 | LIME | William Bendinelli | 2026-08-24 — presented | **[available](modules/14-lime/)** |
| 15 | Counterfactual Explanations | Paulo Alberto Garcia Ferreira | 2026-08-24 — presented | awaited |
| 16 | Scoped Rules (Anchors) | Bruna Campos Guedes | 2026-09-14 | scheduled |
| 17 | Shapley Values | Bruno Rafael Florentino | 2026-08-31 | scheduled |
| 18 | SHAP | Bruno Rafael Florentino | 2026-08-31 | scheduled |
| 19 | Partial Dependence Plot (PDP) | Rômulo Marques Carvalho | 2026-09-14 | scheduled |
| 20 | Accumulated Local Effects (ALE) | Ana Julia Gonzalez Tendulini | 2026-09-21 | scheduled |
| 21 | Feature Interaction | Paulo Alberto Garcia Ferreira | 2026-09-21 | scheduled |
| 22 | Functional Decomposition | Rômulo Marques Carvalho | 2026-10-05 | scheduled |
| 23 | Permutation Feature Importance | William Bendinelli | 2026-10-05 | scheduled |
| 24 | Leave One Feature Out (LOFO) Importance | Bruno Rafael Florentino | 2026-10-19 | scheduled |
| 25 | Surrogate Models | Fabiano Berardo de Sousa | 2026-10-19 | scheduled |
| 26 | Prototypes and Criticisms | Bruna Campos Guedes | 2026-10-26 | scheduled |
| 27 | Learned Features | Ana Julia Gonzalez Tendulini | 2026-10-26 | scheduled |
| 28 | Saliency Maps | Paulo Alberto Garcia Ferreira | 2026-11-09 | scheduled |
| 29 | Detecting Concepts | William Bendinelli | 2026-11-09 | scheduled |
| 30 | Adversarial Examples | Fabiano Berardo de Sousa | 2026-11-16 | scheduled |
| 31 | Influential Instances | Bruna Campos Guedes | 2026-11-16 | scheduled |
| 32 | Evaluation of Interpretability Methods | Rômulo Marques Carvalho | 2026-11-23 | scheduled |
| 34 | The Future of Interpretability | Prof. Dr. André C. P. L. F. de Carvalho | 2026-11-23 | — |

No sessions on 2026-09-07, 2026-09-28, 2026-10-12, 2026-11-02.
<!-- board:end -->

Module numbers are Molnar's chapter numbers, so the mapping between a lecture and its chapter never drifts. Claim or discuss a chapter via the [new-module issue form](https://github.com/scc5819/interpretable-ml-lectures/issues/new/choose). Modules for chapters 27–31 (neural network interpretation) will need a case of their own, since the shared case below is a tabular model — say what it is in the proposal. Chapters 33–34 are essays rather than methods: 33 is skipped in the course, and 34 closes it without a module slot. The table above is generated from [`schedule.toml`](schedule.toml) — edit that file, never the table.

Every module is self-contained: its own notebooks, figures, lecture outline, references, and README. Method-specific citations live in the module that uses them, not here. Modules share one dataset, one model and one patient — the Breast Cancer Wisconsin (Diagnostic) dataset, a RandomForest, and test patient #67 — so the series reads as one continuous case.

## How these materials are built

Two habits keep the material checkable rather than just believable: quantitative claims are printed by the notebooks that make them, and each module pairs its lecture notebook with a technical companion that verifies the method against its own library. Real data and real models throughout — including the measurements that turn out inconvenient.

## Repository map

| Path | What it is |
|---|---|
| [`modules/`](modules/) | one module per Molnar chapter — notebooks, figures, lecture outline, README |
| [`modules/_template/`](modules/_template/) | the starting point for a new module |
| [`schedule.toml`](schedule.toml) | single source of truth for the module board above |
| [`tools/`](tools/) | `render_board.py` (renders the board) and `check_notebooks.py` (notebook conventions) |
| [`tests/`](tests/) | pytest suite for the board tooling |
| [`requirements.txt`](requirements.txt) / [`requirements.lock`](requirements.lock) | the pinned stack — human-readable pins, and the full hash-locked resolution |
| [`CHANGELOG.md`](CHANGELOG.md) | repository-level changes, dated |
| [`CLAUDE.md`](CLAUDE.md) | operating manual for coding agents (and a fine crib sheet for humans) |

## Getting started

**In Colab.** The simplest route: open a module's notebook directly in Google Colab using the badges at the top of that module's README. No local setup — but know the trade-off: **Colab ignores `requirements.txt` entirely** and installs whatever the notebook's unpinned `%pip` cell resolves to that day, so sampling-sensitive third decimals may differ from the committed outputs. The conclusions hold; the bytes may not.

**In Binder.** [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scc5819/interpretable-ml-lectures/main) builds its image from this repository's `requirements.txt`, so unlike Colab it runs the *pinned* package stack (Binder's Python version may still differ from 3.14).

**Locally** (the route the committed numbers were produced on):

```bash
pip install -r requirements.txt          # the pins, human-readable
# or, for an exact environment down to every transitive dependency:
pip install --require-hashes -r requirements.lock
jupyter notebook
```

Then open the notebooks inside the module of interest (e.g. `modules/14-lime/notebooks/`).

## Reproducibility

Notebooks fix their random seeds (`random_state=42` throughout) and state their data splits explicitly. Committed figures and printed numbers were generated with Python 3.14 and the versions recorded in [`requirements.txt`](requirements.txt) — fully resolved, transitive dependencies included, with hashes in [`requirements.lock`](requirements.lock), which is what CI installs; other versions may shift sampling-sensitive results, and the notebooks flag where that matters. The baseline tracks the current stack deliberately: CI runs a weekly canary of the notebooks on the newest Python and unpinned latest packages, and the pins move when a maintainer verifies the numbers survive (the 3.12 → 3.14 upgrade was made exactly that way — every printed output byte-identical).

## Contributing

Corrections, replications, new modules from the table above, clarity edits — all welcome, from anyone. The habit that keeps the material checkable: if a change states a number, it also adds the notebook cell that prints it. [CONTRIBUTING.md](CONTRIBUTING.md) has the setup guide and the module template.

## Citing

Cite via the metadata in [`CITATION.cff`](CITATION.cff) — GitHub renders a "Cite this repository" button from it. Authoring a whole module earns an entry in its `authors` list; every other contribution is credited by the commit history.

## Reference

Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*. [christophm.github.io/interpretable-ml-book](https://christophm.github.io/interpretable-ml-book/)

## Acknowledgments

Course SCC5819 — Topics in Artificial Intelligence, ICMC-USP, taught by Prof. Dr. André Carlos Ponce de Leon Ferreira de Carvalho; the structure and terminology follow Christoph Molnar's *Interpretable Machine Learning*. Module authorship is credited where it lives: each module README's byline, the presenter column of the [module board](#modules), the `authors` list in [`CITATION.cff`](CITATION.cff), and the [contributor graph](https://github.com/scc5819/interpretable-ml-lectures/graphs/contributors) for everything else.

## License

| | License | File |
|---|---|---|
| **Code** — notebook code cells, scripts, CI configuration | MIT | [`LICENSE`](LICENSE) |
| **Content** — prose, lecture outlines, figures, slide decks, notebook markdown cells and printed outputs | CC BY-SA 4.0 | [`LICENSE-CC-BY-SA-4.0.md`](LICENSE-CC-BY-SA-4.0.md) |

A notebook is both: its code cells are MIT; its markdown cells, figures and printed numbers are CC BY-SA 4.0. Reuse the code under MIT; reuse the explanations or figures under share-alike. Quoted passages from the literature belong to their authors and are quoted under citation, not relicensed; the dataset ships with scikit-learn under its own terms.
