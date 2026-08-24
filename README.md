# Interpretable ML — Lecture Materials

[![CI](https://github.com/scc5819/interpretable-ml-lectures/actions/workflows/ci.yml/badge.svg)](https://github.com/scc5819/interpretable-ml-lectures/actions/workflows/ci.yml)

Lecture materials on machine learning interpretability for **SCC5819 — Topics in Artificial Intelligence**, a graduate course at the Institute of Mathematics and Computer Sciences, University of São Paulo (ICMC-USP), Brazil, taught by Prof. Dr. André Carlos Ponce de Leon Ferreira de Carvalho. The materials follow the structure and terminology of the course's reference book, Christoph Molnar's [*Interpretable Machine Learning*](https://christophm.github.io/interpretable-ml-book/), covering it one lecture module per chapter from chapter 12 onward.

Each module covers one method, on real data, with every claim measured rather than asserted.

The repository is maintained by the course community. Corrections, replications and new modules arrive as pull requests, and the evidence bar above applies to all of them — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Modules

One module per chapter of Molnar's book, from chapter 12 on. A module marked *open* is unclaimed: if you presented (or want to present) that method, it is yours to write — see [Adding a new module](CONTRIBUTING.md#adding-a-new-module).

| Module | Method | Status |
|---|---|---|
| 12 — Ceteris paribus | Changing one feature at a time | open — contribution welcome |
| 13 — ICE | Individual conditional expectation curves | open — contribution welcome |
| [**14 — LIME**](modules/14-lime/) | Local Interpretable Model-agnostic Explanations | **available** |
| 15 — Counterfactuals | Counterfactual explanations | open — contribution welcome |
| 16 — Anchors | Scoped rules | open — contribution welcome |
| 17 — Shapley values | Game-theoretic attribution | open — contribution welcome |
| 18 — SHAP | Shapley additive explanations | open — contribution welcome |
| 19 — PDP | Partial dependence plots | open — contribution welcome |
| 20 — ALE | Accumulated local effects | open — contribution welcome |
| 21 — Feature interaction | Interaction strength (H-statistic) | open — contribution welcome |
| 22 — Functional decomposition | Decomposing the prediction function | open — contribution welcome |
| 23 — Permutation importance | Permutation feature importance | open — contribution welcome |
| 24 — LOFO | Leave-one-feature-out importance | open — contribution welcome |
| 25 — Surrogate models | Global surrogates | open — contribution welcome |
| 26 — Prototypes | Prototypes and criticisms | open — contribution welcome |
| 32 — Evaluation | Evaluating interpretability methods | open — contribution welcome |

Module numbers are Molnar's chapter numbers, so the mapping between a lecture and its chapter never drifts. Chapters 27–31 (neural network interpretation) are welcome too — propose one via the [new-module issue form](https://github.com/scc5819/interpretable-ml-lectures/issues/new/choose); they will need a case of their own, since the shared case below is a tabular model. Chapters 33–34 are essays rather than methods, so they carry no module slot.

Every module is self-contained: its own notebooks, figures, lecture outline, references, and README. Method-specific citations live in the module that uses them, not here. Modules share one dataset, one model and one patient — the Breast Cancer Wisconsin (Diagnostic) dataset, a RandomForest, and test patient #67 — so the series reads as one continuous case.

## How these materials are built

The same commitments apply to every module, and they are what the repository is for:

- **Real data and real models.** No toy illustrations standing in for the method. If a figure shows a decision boundary, it is the model's actual decision boundary, computed rather than sketched.
- **Every number is measured where it is stated.** Quantitative claims in a lecture are printed by the notebook that makes them, so a student can check any of them.
- **Each module pairs a lecture with a technical companion.** The lecture notebook teaches; a second notebook validates the implementation against the source code of the library being used, and measures the method's behavior independently of what its documentation promises.
- **Limitations are measured, including inconvenient ones.** Where a method's standard framing does not survive testing, the material says so and shows the measurement — even when that undercuts the tidier version of the lesson.

## Getting started

**In Colab.** The simplest route: open a module's notebook directly in Google Colab using the badge at the top of that module's README. No local setup.

**Locally.**

```bash
pip install -r requirements.txt
jupyter notebook
```

Then open the notebooks inside the module of interest (e.g. `modules/14-lime/notebooks/`).

## Reproducibility

Notebooks fix their random seeds (`random_state=42` throughout) and state their data splits explicitly. Committed figures and printed numbers were generated with Python 3.14 and the versions recorded in [`requirements.txt`](requirements.txt); other versions may shift sampling-sensitive results, and the notebooks flag where that matters. The baseline tracks the current stack deliberately: CI runs a weekly canary of the notebooks on the newest Python and unpinned latest packages, and the pins move when a maintainer verifies the numbers survive (the 3.12 → 3.14 upgrade was made exactly that way — every printed output byte-identical).

## Contributing

In priority order: a **measurement that falsifies a claim here** is the most valuable contribution; then replications on other datasets and models, corrections, new modules from the table above, and clarity edits. The one hard rule: a pull request that adds a claim must add the notebook cell that prints it. [CONTRIBUTING.md](CONTRIBUTING.md) has the first-steps guide, the evidence bar in full, and the module template; conduct is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## Citing

Cite via the metadata in [`CITATION.cff`](CITATION.cff) — GitHub renders a "Cite this repository" button from it. Authoring a whole module earns an entry in its `authors` list; every other contribution is credited by the commit history.

## Reference

Molnar, C. *Interpretable Machine Learning: A Guide for Making Black Box Models Explainable*. [christophm.github.io/interpretable-ml-book](https://christophm.github.io/interpretable-ml-book/)

## Acknowledgments

Course SCC5819 — Topics in Artificial Intelligence, ICMC-USP, taught by Prof. Dr. André Carlos Ponce de Leon Ferreira de Carvalho. The LIME module was written by William Bendinelli as the course's seminar material and originated in [wbendinelli/interpretable-ml-lectures](https://github.com/wbendinelli/interpretable-ml-lectures); the structure and terminology follow Christoph Molnar's *Interpretable Machine Learning*. Everyone who has contributed since is in the repository's [contributor graph](https://github.com/scc5819/interpretable-ml-lectures/graphs/contributors).

## License

| | License | File |
|---|---|---|
| **Code** — notebook code cells, scripts, CI configuration | MIT | [`LICENSE`](LICENSE) |
| **Content** — prose, lecture outlines, figures, slide decks, notebook markdown cells and printed outputs | CC BY-SA 4.0 | [`LICENSE-CC-BY-SA-4.0.md`](LICENSE-CC-BY-SA-4.0.md) |

A notebook is both: its code cells are MIT; its markdown cells, figures and printed numbers are CC BY-SA 4.0. Reuse the code under MIT; reuse the explanations or figures under share-alike. Quoted passages from the literature belong to their authors and are quoted under citation, not relicensed; the dataset ships with scikit-learn under its own terms.
