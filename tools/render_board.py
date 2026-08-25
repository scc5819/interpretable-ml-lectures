#!/usr/bin/env python3
"""Regenerate the module/seminar board in README.md from schedule.toml.

The table's truth depends on three sources: the schedule (schedule.toml),
the calendar (a seminar counts as "presented" from its date onward — the
convention is the date itself, not the day after), and the filesystem (a
module is "available" once modules/<chapter>-*/ exists). This script is the
only writer of the block between the board markers — edit schedule.toml,
never the table.

Usage:
    python3 tools/render_board.py                # rewrite README.md in place
    python3 tools/render_board.py --check        # exit 1 with a diff if stale
    python3 tools/render_board.py --check-static # date-independent subset only,
                                                 # safe to run on PRs

Exit codes: 0 fresh/written · 1 stale (check modes) · 2 broken input
(malformed TOML, missing fields, a modules/ directory with no schedule row).
CI treats 1 as "file an issue" and 2 as a failure — keep them distinct.

Stdlib only; requires Python >= 3.11 (tomllib).
"""

import argparse
import datetime
import difflib
import pathlib
import re
import sys

import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BEGIN, END = "<!-- board:begin -->", "<!-- board:end -->"


class BoardError(Exception):
    """Broken input — distinct from a stale board."""


def module_dir(chapter: int, root: pathlib.Path) -> pathlib.Path | None:
    hits = sorted(p for p in root.glob(f"modules/{chapter}-*") if p.is_dir())
    if len(hits) > 1:
        raise BoardError(
            f"chapter {chapter} matches more than one module directory: "
            + ", ".join(p.name for p in hits)
        )
    return hits[0] if hits else None


def load_schedule(root: pathlib.Path) -> dict:
    schedule = root / "schedule.toml"
    try:
        data = tomllib.loads(schedule.read_text(encoding="utf-8"))
    except OSError as e:
        raise BoardError(f"cannot read {schedule}: {e}") from e
    except tomllib.TOMLDecodeError as e:
        raise BoardError(f"{schedule} is not valid TOML: {e}") from e

    if "chapters" not in data or "no_sessions" not in data:
        raise BoardError(f"{schedule} must define both [[chapters]] and no_sessions")
    for i, c in enumerate(data["chapters"]):
        for field in ("chapter", "title", "date"):
            if field not in c:
                raise BoardError(f"{schedule}: chapters[{i}] is missing '{field}'")
        if not isinstance(c["date"], datetime.date) or isinstance(
            c["date"], datetime.datetime
        ):
            raise BoardError(
                f"{schedule}: chapters[{i}].date must be a local date (YYYY-MM-DD)"
            )
    seen = [c["chapter"] for c in data["chapters"]]
    if len(seen) != len(set(seen)):
        raise BoardError(f"{schedule}: duplicate chapter numbers")

    # Every modules/NN-* directory must have a schedule row, or the board
    # silently ignores it.
    known = set(seen)
    for p in sorted(root.glob("modules/*")):
        m = re.match(r"(\d+)-", p.name)
        if p.is_dir() and m and int(m.group(1)) not in known:
            raise BoardError(
                f"{p} has no matching chapter in {schedule} — the board would not show it"
            )
    return data


def render(today: datetime.date, root: pathlib.Path = ROOT) -> str:
    data = load_schedule(root)
    chapters = sorted(data["chapters"], key=lambda c: c["chapter"])

    rows, available, presented, upcoming = [], 0, 0, []
    module_slots = [c for c in chapters if not c.get("no_module")]
    for c in chapters:
        date = c["date"]
        is_past = date <= today
        presented += is_past
        if not is_past:
            upcoming.append(c)

        seminar = f"{date} — presented" if is_past else str(date)
        mdir = None if c.get("no_module") else module_dir(c["chapter"], root)
        if mdir is not None:
            module = f"**[available]({mdir.relative_to(root).as_posix()}/)**"
            available += 1
        elif c.get("no_module"):
            module = "—"
        elif c.get("presenter") is None:
            module = "open — contribution welcome"
        elif is_past:
            module = "awaited"
        else:
            module = "scheduled"
        rows.append(
            f"| {c['chapter']} | {c['title']} | {c.get('presenter') or '—'} "
            f"| {seminar} | {module} |"
        )

    if upcoming:
        next_date = min(c["date"] for c in upcoming)
        chs = ", ".join(str(c["chapter"]) for c in upcoming if c["date"] == next_date)
        next_line = f" · next session {next_date} (ch. {chs})"
    else:
        next_line = ""
    state = (
        f"**{available} of {len(module_slots)} modules available** · "
        f"{presented} of {len(chapters)} seminars presented{next_line}."
    )

    no_sessions = ", ".join(str(d) for d in data["no_sessions"])
    return "\n".join(
        [
            BEGIN,
            "<!-- Generated — edit schedule.toml and run:  python3 tools/render_board.py",
            "     Do not edit this block by hand. -->",
            state,
            "",
            "| Ch. | Method | Presenter | Seminar | Module |",
            "|---|---|---|---|---|",
            *rows,
            "",
            f"No sessions on {no_sessions}.",
            END,
        ]
    )


def static_view(block: str) -> str:
    """Strip the date-dependent parts of a board block.

    What survives is checkable on any day: chapters, titles, presenters,
    seminar dates, module availability, the no-session list. What is removed
    is what the calendar moves: presented markers/counts, awaited-vs-scheduled,
    and the next-session pointer.
    """
    block = re.sub(r" — presented", "", block)
    block = re.sub(r"\b(awaited|scheduled)\b", "pending", block)
    block = re.sub(r"\d+ of \d+ seminars presented", "seminars", block)
    block = re.sub(r" · next session [0-9-]+ \(ch\. [0-9, ]+\)", "", block)
    return block


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if README is stale")
    mode.add_argument(
        "--check-static",
        action="store_true",
        help="fail only on date-independent drift (safe on PRs)",
    )
    args = ap.parse_args()

    readme = ROOT / "README.md"
    old = readme.read_text(encoding="utf-8")
    if BEGIN not in old or END not in old:
        print(f"markers {BEGIN} / {END} not found in {readme}", file=sys.stderr)
        return 2
    try:
        # The course calendar is a local date by design; timezone-aware "now"
        # would move the presented flag at a different midnight than ICMC's.
        block = render(datetime.date.today())  # noqa: DTZ011
    except BoardError as e:
        print(f"schedule error: {e}", file=sys.stderr)
        return 2
    new = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        lambda _: block,
        old,
        count=1,
        flags=re.DOTALL,
    )

    if args.check or args.check_static:
        left, right = (old, new)
        if args.check_static:
            left, right = static_view(old), static_view(new)
        if left != right:
            sys.stderr.writelines(
                difflib.unified_diff(
                    left.splitlines(keepends=True),
                    right.splitlines(keepends=True),
                    "README.md (committed)",
                    "README.md (regenerated)",
                )
            )
            return 1
        print("board is fresh" if args.check else "board is fresh (static view)")
        return 0

    if new != old:
        readme.write_text(new, encoding="utf-8")
        print("README.md board regenerated")
    else:
        print("board already fresh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
