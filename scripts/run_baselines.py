#!/usr/bin/env python3
"""Run deterministic AMR-Bench-mini baselines and score them."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.baselines import rule_baseline  # noqa: E402
from amr_bench.io import read_jsonl, write_json, write_jsonl  # noqa: E402
from amr_bench.scoring import aggregate_scores, score_output, summary_markdown  # noqa: E402

TASKS = ROOT / "data" / "tasks"
RESULTS = ROOT / "results"


def main() -> None:
    tasks = (
        read_jsonl(TASKS / "genopheno.jsonl")
        + read_jsonl(TASKS / "dbreconcile.jsonl")
        + read_jsonl(TASKS / "mechreason.jsonl")
    )
    if not tasks:
        raise SystemExit("No tasks found. Run scripts/build_tasks.py first.")

    rows = []
    scored = []
    for task in tasks:
        output = rule_baseline(task)
        score = score_output(task, output)
        rows.append({"model": "rule_baseline", "task": task, "output": output, "score": score})
        scored.append(score)

    summary = aggregate_scores(scored)
    write_jsonl(RESULTS / "rule_baseline.jsonl", rows)
    write_json(RESULTS / "rule_baseline_summary.json", summary)
    (RESULTS / "rule_baseline_summary.md").write_text(summary_markdown(summary))

    print(f"Scored {len(rows)} tasks -> {RESULTS / 'rule_baseline.jsonl'}")
    print(summary_markdown(summary))


if __name__ == "__main__":
    main()
