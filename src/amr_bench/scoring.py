"""Scoring utilities for AMR-Bench-mini."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from amr_bench.parsing import norm_gene
from amr_bench.schema import MECHREASON_LAYERS, validate_output


def normalize_label(value: Any) -> str:
    return str(value or "").strip().lower()


def score_output(task: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    errors = validate_output(output)
    result: dict[str, Any] = {
        "task_id": task.get("task_id"),
        "track": task.get("track"),
        "json_valid": not errors,
        "format_errors": errors,
        "correct": False,
        "evidence_items": len(output.get("evidence", [])) if isinstance(output.get("evidence"), list) else 0,
        "confidence": output.get("confidence"),
    }
    if errors:
        return result

    if task.get("track") == "genopheno":
        gold = normalize_label(task.get("gold", {}).get("phenotype"))
        pred = normalize_label(output.get("phenotype_prediction") or output.get("answer"))
        result["gold"] = gold
        result["prediction"] = pred
        result["correct"] = pred == gold
        return result

    if task.get("track") == "dbreconcile":
        gold = normalize_label(task.get("gold", {}).get("disagreement_type"))
        pred = normalize_label(output.get("disagreement_type") or output.get("answer"))
        result["gold"] = gold
        result["prediction"] = pred
        result["correct"] = pred == gold
        return result

    if task.get("track") == "mechreason":
        return score_mechreason(task, output, result)

    return result


def score_mechreason(task: dict[str, Any], output: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Rubric-style scoring for MechReason: 3 binary checks + a tools_called flag.

    Binary subscores:
      - mechanism_class_correct : the predicted mechanism_class matches gold.
      - gene_family_correct     : at least one required gene family appears in the model's evidence list.
      - layers_complete         : the rationale or layered output mentions all five L1..L5 scales.
    A composite "correct" flag is awarded when all three binary checks pass.
    """
    gold = task.get("gold", {})
    gold_class = normalize_label(gold.get("mechanism_class"))
    pred_class = normalize_label(output.get("mechanism_class") or output.get("answer"))

    required = {norm_gene(str(g)) for g in gold.get("required_genes", []) if g}

    evidence_text = " ".join(
        " ".join(str(item.get(field, "")) for field in ("gene", "claim", "source"))
        for item in (output.get("evidence") or [])
        if isinstance(item, dict)
    )
    evidence_compact = norm_gene(evidence_text)
    gene_family_correct = bool(required) and any(req and req in evidence_compact for req in required)

    layered = output.get("layers") if isinstance(output.get("layers"), dict) else {}
    rationale_text = str(output.get("rationale") or "").lower()
    layers_present: list[str] = []
    for layer in MECHREASON_LAYERS:
        if layer in layered and str(layered[layer]).strip():
            layers_present.append(layer)
        elif layer in rationale_text:
            layers_present.append(layer)
    layers_complete = len(layers_present) == len(MECHREASON_LAYERS)

    mechanism_class_correct = pred_class == gold_class and bool(gold_class)
    composite = mechanism_class_correct and (gene_family_correct or pred_class == "insufficient_evidence") and layers_complete

    tools_called = bool(output.get("tools_called"))

    result.update(
        {
            "gold": gold_class,
            "prediction": pred_class,
            "correct": composite,
            "mechanism_class_correct": mechanism_class_correct,
            "gene_family_correct": gene_family_correct,
            "layers_complete": layers_complete,
            "layers_present": layers_present,
            "tools_called": tools_called,
        }
    )
    return result


def aggregate_scores(scored: list[dict[str, Any]]) -> dict[str, Any]:
    by_track: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        by_track[str(row.get("track"))].append(row)

    summary: dict[str, Any] = {"overall": summarize_rows(scored), "by_track": {}}
    for track, rows in sorted(by_track.items()):
        summary["by_track"][track] = summarize_rows(rows)
    return summary


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    if n == 0:
        return {"n": 0}
    valid = [row for row in rows if row.get("json_valid")]
    correct = [row for row in rows if row.get("correct")]
    evidence_counts = [int(row.get("evidence_items", 0)) for row in rows]
    return {
        "n": n,
        "json_valid_rate": round(len(valid) / n, 4),
        "accuracy": round(len(correct) / n, 4),
        "mean_evidence_items": round(sum(evidence_counts) / n, 4),
    }


def summary_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Rule Baseline Summary",
        "",
        "| Split | n | JSON valid | Accuracy | Mean evidence items |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    overall = summary.get("overall", {})
    lines.append(format_summary_row("overall", overall))
    for track, row in summary.get("by_track", {}).items():
        lines.append(format_summary_row(track, row))
    lines.append("")
    return "\n".join(lines)


def format_summary_row(name: str, row: dict[str, Any]) -> str:
    return (
        f"| {name} | {row.get('n', 0)} | {row.get('json_valid_rate', 0):.4f} | "
        f"{row.get('accuracy', 0):.4f} | {row.get('mean_evidence_items', 0):.4f} |"
    )
