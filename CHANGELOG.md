# Changelog

Notable changes to the repository as a whole. Module-level content changes are
tracked in the git history under their `docs(NN-slug)`/`fix(NN-slug)` scopes.

## 2026-08-25 — peer voice

- Removed the Code of Conduct, SECURITY.md and SUPPORT.md, and rewrote
  CONTRIBUTING and the README's framing sections in a peer voice: this is a
  repository among course colleagues, and authority-toned governance was
  hurting engagement. The quality bar did not move — CI still executes the
  notebooks and checks every convention on every PR; the evidence bar stays
  in CONTRIBUTING as three short rules. Private contact now lives in
  CONTRIBUTING's Contact section.

## 2026-08-25 — agent operating manual

- Removed the devcontainer: Colab, Binder and the lockfile cover every real
  use; an exact-interpreter route nobody uses is maintenance, not value.

- `CLAUDE.md` (with an `AGENTS.md` pointer): the condensed operating manual
  for coding agents — what CI enforces, the duties no check can enforce
  (CHANGELOG, board regeneration, the notebook re-run protocol, figure
  promotion, prose↔cell sync, the 03-lime mirror), and the changes that look
  like improvements but are policy violations here.
- CI now enforces the CHANGELOG discipline: a PR touching `modules/`,
  `tools/`, `.github/` or `requirements*` must touch `CHANGELOG.md` too
  (escape hatch: the `no-changelog` label, added to `labels.toml`).
- README: repository map, devcontainer route in Getting started, and the
  Acknowledgments now credit module authorship where it lives (bylines, the
  board, `CITATION.cff`) instead of naming authors inline.

## 2026-08-24 — audit fixes

An external audit of the repository (structure, CI, governance, and a
line-by-line review of the LIME module against the `lime` 0.2.0.1 sdist and
Molnar's book) produced a prioritized backlog; this batch lands it.

### Content (module 14)
- Fixed the kernel-ring figures: the individual step figures now lock the data
  rectangle like the combined figure, so the 0.95-weight contour draws as the
  circle it is and fits the frame — the prose said so, the pixels did not.
- Replaced "g(x) lands near 0.5 almost regardless of patient" (contradicted by
  the printed table) with the accurate claim: g shrinks toward the cloud mean.
- Every number quoted in `lecture/outline.md` is now printed by a committed
  cell — a new internals §12 appendix measures the ones that were not
  (seed × num_features sweep, 30-feature refit, `discretize_continuous=True`,
  R² seed sensitivity, the Clopper–Pearson interval).
- §9b now prints the real per-scenario n (wine has 33 test points, not 55) and
  declares its model differences; cross-references fixed ("module 02" → the
  chapter 13 seminar, "slide 21" → 18, "Break 1" → the deck's second act).

### Infrastructure
- `requirements.lock`: full transitive resolution with hashes; CI installs it.
- CI: actions pinned to commit SHAs and bumped to current majors; weekly issue
  filing now updates one tracking issue instead of duplicating; the scheduled
  run no longer shares a concurrency group with pushes; lychee accepts 403;
  Python pinned to 3.14.6; a `checks` job runs pre-commit and the board tests.
- `tools/render_board.py`: distinct exit codes (stale=1, broken input=2),
  schedule validation, orphan-module detection, a date-independent
  `--check-static` mode that runs on every PR, and a pytest suite.
- `tools/check_notebooks.py` + pre-commit: the notebook conventions from
  CONTRIBUTING (execution counts 1..N, unpinned `%pip`, no `%%time`) are now
  machine-checked.
- Governance: private conduct-report channel in the Code of Conduct;
  SECURITY.md, SUPPORT.md, `.gitattributes`, `.editorconfig`, Dependabot for
  the actions ecosystem only, a devcontainer, and Binder as a pinned-stack
  alternative to Colab.
