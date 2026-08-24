#!/usr/bin/env python3
"""Regenerate the module/seminar board in README.md from schedule.toml.

The table's truth depends on three sources: the schedule (schedule.toml),
the calendar (a seminar is "presented" once its date passes), and the
filesystem (a module is "available" once modules/<chapter>-*/ exists).
This script is the only writer of the block between the board markers —
edit schedule.toml, never the table.

Usage:
    python3 tools/render_board.py           # rewrite README.md in place
    python3 tools/render_board.py --check   # exit 1 with a diff if stale

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
README = ROOT / "README.md"
SCHEDULE = ROOT / "schedule.toml"
BEGIN, END = "<!-- board:begin -->", "<!-- board:end -->"


def module_dir(chapter: int) -> pathlib.Path | None:
    hits = sorted(ROOT.glob(f"modules/{chapter}-*/"))
    return hits[0] if hits else None


def render(today: datetime.date) -> str:
    data = tomllib.loads(SCHEDULE.read_text(encoding="utf-8"))
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
        mdir = module_dir(c["chapter"])
        if mdir is not None:
            module = f"**[available]({mdir.relative_to(ROOT).as_posix()}/)**"
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if README is stale")
    args = ap.parse_args()

    old = README.read_text(encoding="utf-8")
    if BEGIN not in old or END not in old:
        sys.exit(f"markers {BEGIN} / {END} not found in {README}")
    block = render(datetime.date.today())
    new = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block, old, flags=re.S
    )

    if args.check:
        if new != old:
            sys.stderr.writelines(
                difflib.unified_diff(
                    old.splitlines(keepends=True),
                    new.splitlines(keepends=True),
                    "README.md (committed)",
                    "README.md (regenerated)",
                )
            )
            return 1
        print("board is fresh")
        return 0

    if new != old:
        README.write_text(new, encoding="utf-8")
        print("README.md board regenerated")
    else:
        print("board already fresh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
