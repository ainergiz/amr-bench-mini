#!/usr/bin/env python3
"""Re-score raw_outputs.jsonl from past runs against both strict and adjusted gold.

For each run directory under results/llm_eval/, this script:
  - Re-scores the saved model outputs against data/tasks/mechreason_strict.jsonl (strict)
    and data/tasks/mechreason.jsonl (adjusted).
  - Writes summary_strict.json and summary_adjusted.json next to the existing summary.json.
  - Writes a side-by-side comparison summary_compare.md.

The original raw_outputs.jsonl, summary.json, and summary.md are not modified.

Usage:
    python3 scripts/rescore_runs.py                    # all runs
    python3 scripts/rescore_runs.py <run_dir> ...      # specific runs
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl, write_json  # noqa: E402
from amr_bench.scoring import aggregate_scores, score_output  # noqa: E402

LLM_EVAL = ROOT / "results" / "llm_eval"
TASKS = ROOT / "data" / "tasks"


def load_gold_index(jsonl_path: Path) -> dict:
    return {t["task_id"]: t for t in read_jsonl(jsonl_path)}


def rescore_run(run_dir: Path, strict_idx: dict, adjusted_idx: dict) -> dict | None:
    raw_path = run_dir / "raw_outputs.jsonl"
    if not raw_path.exists():
        return None
    rows = read_jsonl(raw_path)
    if not rows:
        return None

    strict_scored: list[dict] = []
    adjusted_scored: list[dict] = []
    by_task_strict: dict[str, dict] = {}
    by_task_adjusted: dict[str, dict] = {}

    for row in rows:
        tid = row["task_id"]
        output = row.get("output") or {}
        if tid in strict_idx:
            s = score_output(strict_idx[tid], output)
            strict_scored.append(s)
            by_task_strict[tid] = s
        if tid in adjusted_idx:
            a = score_output(adjusted_idx[tid], output)
            adjusted_scored.append(a)
            by_task_adjusted[tid] = a

    if not strict_scored or not adjusted_scored:
        return None

    strict_summary = aggregate_scores(strict_scored)
    adjusted_summary = aggregate_scores(adjusted_scored)
    strict_summary["mechreason_breakdown"] = mechreason_breakdown(rows, strict_idx)
    adjusted_summary["mechreason_breakdown"] = mechreason_breakdown(rows, adjusted_idx)

    flips = []
    for tid, s in by_task_strict.items():
        a = by_task_adjusted.get(tid)
        if not a:
            continue
        if s.get("correct") != a.get("correct"):
            flips.append({
                "task_id": tid,
                "strict_gold": s.get("gold"),
                "adjusted_gold": a.get("gold"),
                "prediction": s.get("prediction"),
                "strict_correct": s.get("correct"),
                "adjusted_correct": a.get("correct"),
            })

    write_json(run_dir / "summary_strict.json", strict_summary)
    write_json(run_dir / "summary_adjusted.json", adjusted_summary)
    write_json(run_dir / "rescore_flips.json", {"n_flips": len(flips), "flips": flips})

    md = render_compare_md(run_dir.name, strict_summary, adjusted_summary, flips)
    (run_dir / "summary_compare.md").write_text(md)

    return {
        "run": run_dir.name,
        "n_strict": len(strict_scored),
        "n_adjusted": len(adjusted_scored),
        "strict_acc": strict_summary["overall"]["accuracy"],
        "adjusted_acc": adjusted_summary["overall"]["accuracy"],
        "n_flips": len(flips),
    }


def mechreason_breakdown(rows: list[dict], gold_idx: dict) -> dict:
    classes: defaultdict = defaultdict(lambda: {"n": 0, "correct": 0, "mech_correct": 0})
    layer_totals = {"mechanism_class_correct": 0, "gene_family_correct": 0, "layers_complete": 0}
    n = 0
    parse_errors = 0
    for r in rows:
        tid = r["task_id"]
        if tid not in gold_idx:
            continue
        task = gold_idx[tid]
        if task.get("track") != "mechreason":
            continue
        s = score_output(task, r.get("output") or {})
        cls = task["gold"]["mechanism_class"]
        classes[cls]["n"] += 1
        if s.get("correct"):
            classes[cls]["correct"] += 1
        if s.get("mechanism_class_correct"):
            classes[cls]["mech_correct"] += 1
        for k in layer_totals:
            if s.get(k):
                layer_totals[k] += 1
        if (r.get("output") or {}).get("__parse_error") or (r.get("output") or {}).get("__call_error"):
            parse_errors += 1
        n += 1
    return {
        "n_mechreason": n,
        "by_class": {
            cls: {
                **v,
                "accuracy": (v["correct"] / v["n"]) if v["n"] else 0.0,
                "mech_class_accuracy": (v["mech_correct"] / v["n"]) if v["n"] else 0.0,
            }
            for cls, v in classes.items()
        },
        "subscore_rates": {k: (v / n if n else 0.0) for k, v in layer_totals.items()},
        "parse_or_call_errors": parse_errors,
    }


def render_compare_md(run_name: str, strict: dict, adjusted: dict, flips: list[dict]) -> str:
    so = strict["overall"]
    ao = adjusted["overall"]
    lines = [
        f"# Strict vs adjusted rescoring — {run_name}",
        "",
        "Original `summary.json` is untouched. The strict score uses the pre-adjudication gold "
        "(`data/tasks/mechreason_strict.jsonl`); the adjusted score uses the audit-adjudicated gold "
        "(`data/tasks/mechreason.jsonl`).",
        "",
        "| Metric | Strict | Adjusted |",
        "| --- | ---: | ---: |",
        f"| Composite accuracy | {so['accuracy']:.4f} ({int(round(so['accuracy']*so['n']))}/{so['n']}) | {ao['accuracy']:.4f} ({int(round(ao['accuracy']*ao['n']))}/{ao['n']}) |",
        f"| JSON valid rate | {so['json_valid_rate']:.4f} | {ao['json_valid_rate']:.4f} |",
        f"| Mean evidence items | {so['mean_evidence_items']:.4f} | {ao['mean_evidence_items']:.4f} |",
        "",
        "## MechReason — per-class composite accuracy",
        "",
        "| Class | n strict | strict acc | n adjusted | adjusted acc |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    sb = strict.get("mechreason_breakdown", {}).get("by_class", {})
    ab = adjusted.get("mechreason_breakdown", {}).get("by_class", {})
    classes = sorted(set(sb.keys()) | set(ab.keys()))
    for cls in classes:
        s = sb.get(cls, {"n": 0, "accuracy": 0.0})
        a = ab.get(cls, {"n": 0, "accuracy": 0.0})
        lines.append(f"| `{cls}` | {s['n']} | {s.get('accuracy', 0):.4f} | {a['n']} | {a.get('accuracy', 0):.4f} |")

    lines += ["", f"## Score flips ({len(flips)})", ""]
    if flips:
        lines.append("| task_id | strict_gold | adjusted_gold | prediction | strict | adjusted |")
        lines.append("| --- | --- | --- | --- | :-: | :-: |")
        for f in flips:
            sc = "✓" if f["strict_correct"] else "✗"
            ac = "✓" if f["adjusted_correct"] else "✗"
            lines.append(
                f"| {f['task_id']} | `{f['strict_gold']}` | `{f['adjusted_gold']}` | "
                f"`{f['prediction']}` | {sc} | {ac} |"
            )
    else:
        lines.append("*No flips between strict and adjusted scoring.*")

    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("runs", nargs="*", help="Specific run directories. If empty, processes all.")
    args = ap.parse_args()

    strict_idx = load_gold_index(TASKS / "mechreason_strict.jsonl")
    adjusted_idx = load_gold_index(TASKS / "mechreason.jsonl")

    if args.runs:
        run_dirs = [Path(p) for p in args.runs]
    else:
        run_dirs = [p for p in LLM_EVAL.iterdir() if p.is_dir()]

    results = []
    for run_dir in sorted(run_dirs):
        out = rescore_run(run_dir, strict_idx, adjusted_idx)
        if out:
            results.append(out)
            print(
                f"{run_dir.name:60s} strict={out['strict_acc']:.3f} "
                f"adj={out['adjusted_acc']:.3f} flips={out['n_flips']}"
            )
        else:
            print(f"{run_dir.name:60s} (skipped — no raw_outputs)")

    write_json(LLM_EVAL / "rescore_index.json", {"runs": results})
    print(f"\nIndex written to {LLM_EVAL / 'rescore_index.json'}")


if __name__ == "__main__":
    main()
