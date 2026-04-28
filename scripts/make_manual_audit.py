#!/usr/bin/env python3
"""Create a TSV queue for manual failure-mode auditing."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl  # noqa: E402

RESULTS = ROOT / "results"


FIELDS = [
    "task_id",
    "track",
    "model",
    "gold",
    "prediction",
    "automatic_correct",
    "confidence",
    "evidence_items",
    "answer_correct",
    "evidence_valid",
    "hallucinated_gene",
    "hallucinated_source",
    "wrong_antibiotic_class",
    "overconfident",
    "clinical_overclaim",
    "notes",
]


def main() -> None:
    rows = read_jsonl(RESULTS / "rule_baseline.jsonl")
    if not rows:
        raise SystemExit("No baseline rows found. Run scripts/run_baselines.py first.")

    scored = []
    for row in rows:
        score = row["score"]
        scored.append(
            {
                "task_id": score.get("task_id"),
                "track": score.get("track"),
                "model": row.get("model", "rule_baseline"),
                "gold": score.get("gold", ""),
                "prediction": score.get("prediction", ""),
                "automatic_correct": score.get("correct", ""),
                "confidence": score.get("confidence", ""),
                "evidence_items": score.get("evidence_items", 0),
                "answer_correct": "",
                "evidence_valid": "",
                "hallucinated_gene": "",
                "hallucinated_source": "",
                "wrong_antibiotic_class": "",
                "overconfident": "",
                "clinical_overclaim": "",
                "notes": "",
            }
        )

    audit_rows = select_audit_rows(scored)
    out = RESULTS / "manual_audit.tsv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t")
        writer.writeheader()
        writer.writerows(audit_rows)
    print(f"Wrote {len(audit_rows)} audit rows -> {out}")


def select_audit_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []

    def add(track: str, correct: bool, limit: int) -> None:
        matches = [row for row in rows if row["track"] == track and row["automatic_correct"] is correct]
        selected.extend(matches[:limit])

    add("genopheno", False, 10)
    add("genopheno", True, 10)
    add("dbreconcile", True, 10)

    seen: set[str] = set()
    deduped: list[dict[str, object]] = []
    for row in selected:
        key = str(row["task_id"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


if __name__ == "__main__":
    main()
