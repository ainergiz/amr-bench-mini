#!/usr/bin/env python3
"""Backfill cost_estimate_usd onto existing summary.json files in results/llm_eval/.

Reads each run's existing usage_totals + provider + model and adds (or refreshes)
the ``cost_estimate_usd`` field using the shared price table.
Skips runs where summary.json already has a cost estimate from the batch script.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import write_json  # noqa: E402
from amr_bench.pricing import cost_estimate  # noqa: E402

LLM_EVAL = ROOT / "results" / "llm_eval"


def main() -> None:
    for run_dir in sorted(LLM_EVAL.iterdir()):
        if not run_dir.is_dir():
            continue
        summary_path = run_dir / "summary.json"
        if not summary_path.exists():
            continue
        summary = json.loads(summary_path.read_text())
        provider = summary.get("provider")
        model = summary.get("model")
        usage = summary.get("usage_totals") or {}
        if not (provider and model):
            continue
        is_batch = "batch_id" in summary
        new_cost = cost_estimate(model, provider, usage, is_batch=is_batch)
        old = summary.get("cost_estimate_usd")
        summary["cost_estimate_usd"] = new_cost
        write_json(summary_path, summary)
        msg = "updated" if old != new_cost else "unchanged"
        print(f"{run_dir.name:60s} {msg} (input={new_cost.get('input_tokens',0)}, output={new_cost.get('output_tokens',0)})")


if __name__ == "__main__":
    main()
