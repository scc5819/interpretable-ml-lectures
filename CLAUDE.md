# CLAUDE.md — operating manual for agents working in this repository

Lecture materials for SCC5819 (Interpretable ML, ICMC-USP), one module per
chapter of Molnar's *Interpretable Machine Learning* from chapter 12 on.
The repository has **one hard rule** and everything else serves it:

> **Every quantitative claim in prose is printed by a committed notebook cell
> in the same module.** A number without a printing cell is a bug — either add
> the cell or delete the number. When a measurement contradicts the prose, the
> prose changes and the old value stays in the record, marked as corrected
> (evidence bar, rule 3 — see CONTRIBUTING.md).

Full contributor policy: [CONTRIBUTING.md](CONTRIBUTING.md). This file is the
condensed, agent-facing version plus the duties no check enforces.

## What CI already enforces (don't fight it, don't duplicate it)

Red checks are correct behavior — fix the cause, never weaken the check:

- **links** — relative links and anchors in every `.md` + `CITATION.cff`.
- **checks** — pre-commit (ruff on `tools/`, codespell, actionlint, yaml/toml,
  `tools/check_notebooks.py`: execution counts 1..N, unpinned `%pip`, no
  `%%time`) and `tests/` (pytest for `render_board.py`), plus the board's
  date-independent view (`render_board.py --check-static`).
- **walkthroughs / internals** — the notebooks must run end to end on the
  pinned stack (`requirements.lock`, `--require-hashes`, Python 3.14.6) and
  write nothing into the repo tree.
- **citation** — `CITATION.cff` stays schema-valid.
- **changelog** — a PR touching `modules/`, `tools/`, `.github/` or
  `requirements*` must also touch `CHANGELOG.md`, unless it carries the
  `no-changelog` label. Keep entries short: what changed and why it matters.
- Weekly (not on PRs): external link check, full board check, latest-stack
  canary (`canary.yml`), label sync (`labels.yml` ← `.github/labels.toml`).

## Duties CI cannot enforce (do these without being asked)

1. **CHANGELOG.md** — one line per notable change, under a date heading.
   The CI check makes you touch the file; making the line say something
   useful is on you.
2. **Board** — after editing `schedule.toml` or adding a module directory,
   run `python3 tools/render_board.py` and commit the README change. Never
   edit the board block by hand.
3. **Notebook protocol** — any notebook edit, however small, ends with a full
   fresh-kernel run before committing:

   ```bash
   PIP_DISABLE_PIP_VERSION_CHECK=1 jupyter nbconvert --to notebook \
     --execute --inplace modules/NN-slug/notebooks/<name>.ipynb
   ```

   (The env var matters: without it, pip's upgrade banner bakes a local
   filesystem path into the committed output.) Outputs are committed **by
   design** — never strip them, never add nbstripout, never pin versions in
   the `%pip` cell.
4. **Figures** — notebooks write to `figures_generated/` (git-ignored).
   Promote to `modules/NN-slug/figures/` by explicit copy, and say in the
   commit which cell regenerated the figure and why the picture moved.
   Unchanged figures reproduce byte-identically on the pinned stack — a
   figure that diffs without a code change is a finding, not noise.
5. **Prose ↔ cell sync** — after a re-run, diff every printed number against
   the module README and `lecture/outline.md`. Section pointers use the short
   forms `(walkthrough §N)` / `(internals §N)`.
6. **Mirror** — the LIME module is mirrored in
   `wbendinelli/interpretable-ml-lectures` as `modules/03-lime` (locally:
   `~/Documents/interpretable-ml-lectures`). After content changes to
   `modules/14-lime`, sync the mirror: copy notebooks/figures/outline
   verbatim; in README.md rewrite `Module 14` → `Module 03`,
   `scc5819/interpretable-ml-lectures` → `wbendinelli/interpretable-ml-lectures`,
   `modules/14-lime` → `modules/03-lime`. Decks are already identical.

## Things that look like improvements but are policy violations

- **Editing a delivered deck** (`lecture/*.pdf`). Decks are historical
  artifacts of a talk given by a person on a date — never retro-edited, even
  when a number in them has since been corrected. The living form of the
  lecture is `lecture/outline.md`; corrections go there, with a note that the
  frozen deck differs. (Precedent: the deck's "R² swings 30%" vs the
  measured 26% — outline §5.)
- **Bumping Python packages** or adding Dependabot for pip. Pins move once
  per offering, as a single deliberate PR: `requirements.txt` + regenerated
  `requirements.lock` (`pip-compile --generate-hashes`) + every notebook
  re-run + figures + every quoted number re-checked. Actions bumps are the
  one exception (Dependabot handles them; keep the SHA-pin style).
- **Stripping notebook outputs, adding timestamps/`%%time`/progress bars,**
  or "fixing" the unpinned `%pip` cell — all deliberately the way they are.
- **Flipping GitHub e-mail privacy** to surface a profile e-mail. The private
  contact is the institutional address in CONTRIBUTING's Contact section; the
  account's "keep e-mail private" setting stays on.
- **Re-adding governance boilerplate** (code of conduct, security policy,
  review-expectations sections). Deliberately removed: this is a repository
  among course colleagues, and authority-toned documents were hurting
  engagement. CI carries the quality bar; the docs stay in a peer voice.
- **Adding infrastructure.** The repo is at its deliberate infra ceiling
  (CI, pre-commit, lock, board tooling, labels-as-config, canary). New
  investment goes into modules, not machinery.

## Workflow facts

- **Branch → PR → green CI → merge.** `main` is protected; merges go through
  a PR (an admin can `gh pr merge --admin` once CI is green).
- Commit style: `type(scope): summary` — `docs(14-lime): …`,
  `fix(14-lime): …`, `ci: …`, `feat(tools): …`. A falsification is a `fix`.
- Local setup: `python3.14 -m venv .venv && .venv/bin/pip install
  --require-hashes -r requirements.lock` (or `-r requirements.txt` to merely
  follow along). Before pushing: `pre-commit run --all-files`,
  `python3 -m pytest tests/`, `python3 tools/render_board.py --check`.
- Releases: `vYYYY.MM` per course offering (e.g. `v2026.08`), matching
  `version:` in CITATION.cff. Labels are config: edit `.github/labels.toml`,
  the sync workflow applies it on merge.
- Numbers were produced on Apple Silicon + the pinned stack and reproduce
  byte-identically there; a Linux runner may move third decimals, which is
  why CI executes notebooks but never diffs outputs.
