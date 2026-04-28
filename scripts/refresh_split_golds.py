#!/usr/bin/env python3
"""Refresh gold fields inside mechreason_pilot.jsonl and mechreason_hard.jsonl
from data/tasks/mechreason.jsonl, preserving each split's frozen task_id list
and the hard_split metadata.

Strict (pre-adjudication) snapshots live in mechreason_pilot_strict.jsonl and
mechreason_hard_strict.jsonl and are not touched.

Usage:
    python3 scripts/refresh_split_golds.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl, write_jsonl  # noqa: E402

TASKS = ROOT / "data" / "tasks"


def refresh(split_path: Path, full_by_id: dict) -> None:
    split = read_jsonl(split_path)
    updated = []
    diffs = 0
    for task in split:
        canonical = full_by_id[task["task_id"]]
        new_gold = canonical["gold"]
        if task["gold"] != new_gold:
            diffs += 1
        merged = {**task, "gold": new_gold}
        updated.append(merged)
    write_jsonl(split_path, updated)
    print(f"{split_path.name}: {len(updated)} tasks refreshed, {diffs} gold deltas vs. prior content")


def main() -> None:
    full = {t["task_id"]: t for t in read_jsonl(TASKS / "mechreason.jsonl")}
    refresh(TASKS / "mechreason_pilot.jsonl", full)
    refresh(TASKS / "mechreason_hard.jsonl", full)


if __name__ == "__main__":
    main()
