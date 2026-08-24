"""Tests for tools/render_board.py — the only executable code outside notebooks.

Run with:  python3 -m pytest tests/
"""

import datetime
import importlib.util
import pathlib
import sys

import pytest

TOOLS = pathlib.Path(__file__).resolve().parent.parent / "tools"
spec = importlib.util.spec_from_file_location("render_board", TOOLS / "render_board.py")
rb = importlib.util.module_from_spec(spec)
sys.modules["render_board"] = rb
spec.loader.exec_module(rb)

SCHEDULE = """\
no_sessions = [2026-09-07]

[[chapters]]
chapter = 14
title = "LIME"
date = 2026-08-24
presenter = "A"

[[chapters]]
chapter = 15
title = "Counterfactuals"
date = 2026-09-14
presenter = "B"

[[chapters]]
chapter = 34
title = "Essay"
date = 2026-11-23
presenter = "C"
no_module = "essay"
"""


def repo(tmp_path, schedule=SCHEDULE, dirs=("modules/14-lime",)):
    (tmp_path / "schedule.toml").write_text(schedule, encoding="utf-8")
    for d in dirs:
        (tmp_path / d).mkdir(parents=True)
    return tmp_path


def test_render_counts_and_statuses(tmp_path):
    root = repo(tmp_path)
    block = rb.render(datetime.date(2026, 9, 1), root)
    assert "**1 of 2 modules available**" in block
    assert "1 of 3 seminars presented" in block
    assert "| 14 | LIME | A | 2026-08-24 — presented | **[available](modules/14-lime/)** |" in block
    assert "| 15 | Counterfactuals | B | 2026-09-14 | scheduled |" in block
    assert "next session 2026-09-14 (ch. 15)" in block


def test_no_module_chapter_never_counts_as_available(tmp_path):
    # even if a directory exists for it, an essay slot stays "—"
    root = repo(tmp_path, dirs=("modules/14-lime", "modules/34-future"))
    block = rb.render(datetime.date(2026, 9, 1), root)
    assert "**1 of 2 modules available**" in block
    assert "| 34 | Essay | C | 2026-11-23 | — |" in block


def test_orphan_module_dir_is_an_error(tmp_path):
    root = repo(tmp_path, dirs=("modules/14-lime", "modules/99-mystery"))
    with pytest.raises(rb.BoardError, match="99-mystery"):
        rb.render(datetime.date(2026, 9, 1), root)


def test_two_dirs_for_one_chapter_is_an_error(tmp_path):
    root = repo(tmp_path, dirs=("modules/14-lime", "modules/14-lime-v2"))
    with pytest.raises(rb.BoardError, match="more than one"):
        rb.render(datetime.date(2026, 9, 1), root)


def test_malformed_toml_is_an_error(tmp_path):
    root = repo(tmp_path, schedule="chapters = [broken")
    with pytest.raises(rb.BoardError, match="not valid TOML"):
        rb.render(datetime.date(2026, 9, 1), root)


def test_missing_field_is_an_error(tmp_path):
    bad = 'no_sessions = []\n\n[[chapters]]\nchapter = 14\ntitle = "LIME"\n'
    root = repo(tmp_path, schedule=bad, dirs=())
    with pytest.raises(rb.BoardError, match="missing 'date'"):
        rb.render(datetime.date(2026, 9, 1), root)


def test_static_view_is_date_independent(tmp_path):
    root = repo(tmp_path)
    before = rb.render(datetime.date(2026, 8, 20), root)  # nothing presented
    after = rb.render(datetime.date(2026, 12, 1), root)  # everything presented
    assert before != after
    assert rb.static_view(before) == rb.static_view(after)


def test_static_view_sees_real_drift(tmp_path):
    root = repo(tmp_path)
    original = rb.render(datetime.date(2026, 9, 1), root)
    renamed = original.replace("Counterfactuals", "Renamed Chapter")
    assert rb.static_view(original) != rb.static_view(renamed)
