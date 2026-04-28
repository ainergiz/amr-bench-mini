#!/usr/bin/env python3
"""Rebuild MechReason gold from a completed audit_form.tsv.

Usage:
    python3 scripts/apply_audit_overrides.py [--dry-run]

Reads:  results/mechreason_audit/audit_form.tsv
Writes: data/tasks/mechreason.jsonl     (in-place rewrite)
        results/mechreason_audit/override_summary.md   (audit trail)

Behavior:
  - Rows with gold_class_decision == "KEEP" or empty are passed through unchanged.
  - Rows with gold_class_decision == "OVERRIDE" replace gold.mechanism_class
    (and optionally gold.required_genes) on the matching task_id. The proposed
    class must be in VALID_MECHANISM_CLASSES; otherwise the row errors out.
  - Rows with gold_class_decision == "AMBIGUOUS" are left as-is but recorded in
    the override summary with the auditor's note so the paper can carve out
    these cases for separate analysis.

The override summary is the audit trail — keep it under version control so
the published benchmark documents which heuristic labels were corrected by
microbiologist review.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl, write_jsonl  # noqa: E402
from amr_bench.schema import VALID_INTERACTION_TYPES, VALID_MECHANISM_CLASSES  # noqa: E402

DATA = ROOT / "data"
TASKS = DATA / "tasks"
RESULTS = ROOT / "results"
AUDIT_DIR = RESULTS / "mechreason_audit"
AUDIT_FORM = AUDIT_DIR / "audit_form.tsv"
SUMMARY = AUDIT_DIR / "override_summary.md"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Report what would change without writing.")
    args = ap.parse_args()

    if not AUDIT_FORM.exists():
        raise SystemExit(f"No audit form at {AUDIT_FORM}; run scripts/audit_mechreason_labels.py first.")

    overrides: dict[str, dict[str, str]] = {}
    with AUDIT_FORM.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            tid = row["task_id"].strip()
            if not tid:
                continue
            overrides[tid] = row

    tasks = read_jsonl(TASKS / "mechreason.jsonl")
    decision_counter: Counter[str] = Counter()
    override_log: list[dict[str, str]] = []
    errors: list[str] = []

    for task in tasks:
        row = overrides.get(task["task_id"])
        if not row:
            continue
        decision = (row.get("gold_class_decision") or "").strip().upper()
        decision_counter[decision or "(blank)"] += 1
        if decision == "OVERRIDE":
            proposed = (row.get("gold_class_proposed") or "").strip()
            if proposed not in VALID_MECHANISM_CLASSES:
                errors.append(f"{task['task_id']}: proposed class {proposed!r} not in vocabulary")
                continue
            old_class = task["gold"]["mechanism_class"]
            task["gold"]["mechanism_class"] = proposed
            req_decision = (row.get("required_genes_decision") or "").strip().upper()
            if req_decision == "OVERRIDE":
                proposed_genes = [g.strip() for g in (row.get("required_genes_proposed") or "").split(",") if g.strip()]
                old_genes = list(task["gold"]["required_genes"])
                task["gold"]["required_genes"] = proposed_genes
            else:
                old_genes = None
                proposed_genes = None
            apply_optional_hybrid_fields(task, row, errors)
            override_log.append({
                "task_id": task["task_id"],
                "antibiotic": task["antibiotic"],
                "old_class": old_class,
                "new_class": proposed,
                "old_genes": ",".join(old_genes) if old_genes else "",
                "new_genes": ",".join(proposed_genes) if proposed_genes else "",
                "notes": row.get("auditor_notes", ""),
            })
        elif decision == "AMBIGUOUS":
            apply_optional_hybrid_fields(task, row, errors)
            override_log.append({
                "task_id": task["task_id"],
                "antibiotic": task["antibiotic"],
                "old_class": task["gold"]["mechanism_class"],
                "new_class": "(ambiguous, kept)",
                "old_genes": "",
                "new_genes": "",
                "notes": row.get("auditor_notes", ""),
            })

    if errors:
        raise SystemExit("Audit override errors:\n  " + "\n  ".join(errors))

    if not args.dry_run:
        write_jsonl(TASKS / "mechreason.jsonl", tasks)

    write_summary(decision_counter, override_log, dry_run=args.dry_run)

    print("Decision distribution:")
    for k, v in decision_counter.most_common():
        print(f"  {k:>10s}: {v}")
    print(f"\nOverride records: {len(override_log)}")
    if args.dry_run:
        print("(dry-run: no file rewritten)")
    else:
        print(f"Updated {TASKS / 'mechreason.jsonl'}")
        print(f"Wrote   {SUMMARY}")


def apply_optional_hybrid_fields(task: dict, row: dict, errors: list) -> None:
    """Populate gold.secondary_mechanism_classes and gold.interaction_type when
    the auditor has filled the optional columns. Leaves them off otherwise."""
    secondary_raw = (row.get("secondary_classes_proposed") or "").strip()
    interaction_raw = (row.get("interaction_type_proposed") or "").strip().lower()
    if secondary_raw:
        secondary = [c.strip() for c in secondary_raw.split(",") if c.strip()]
        bad = [c for c in secondary if c not in VALID_MECHANISM_CLASSES]
        if bad:
            errors.append(f"{task['task_id']}: invalid secondary classes {bad!r}")
            return
        task["gold"]["secondary_mechanism_classes"] = secondary
    if interaction_raw:
        if interaction_raw not in VALID_INTERACTION_TYPES:
            errors.append(f"{task['task_id']}: invalid interaction_type {interaction_raw!r}")
            return
        task["gold"]["interaction_type"] = interaction_raw


def write_summary(counter: Counter[str], log: list[dict[str, str]], dry_run: bool) -> None:
    lines = [
        "# MechReason Audit Override Summary",
        "",
        f"Generated by scripts/apply_audit_overrides.py{' (dry-run)' if dry_run else ''}.",
        "",
        "## Decision counts",
        "",
        "| Decision | n |",
        "| --- | ---: |",
    ]
    for k, v in counter.most_common():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## Override / ambiguous records")
    lines.append("")
    if not log:
        lines.append("*No overrides or ambiguous decisions recorded.*")
    else:
        lines.append("| task_id | antibiotic | old → new class | old → new genes | notes |")
        lines.append("| --- | --- | --- | --- | --- |")
        for r in log:
            class_str = f"`{r['old_class']}` → `{r['new_class']}`"
            genes_str = f"`{r['old_genes']}` → `{r['new_genes']}`" if r["new_genes"] else ""
            notes = (r["notes"] or "").replace("\n", " ").replace("|", "\\|")
            lines.append(f"| {r['task_id']} | {r['antibiotic']} | {class_str} | {genes_str} | {notes} |")
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
