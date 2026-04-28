#!/usr/bin/env python3
"""Build a deterministic 50-task hard MechReason split.

The hard split is drawn from existing validated MechReason tasks. It emphasizes
cases where gene presence is not enough: evidence insufficiency, intrinsic vs
acquired ontology, regulator LoF vs direct efflux, substrate-specificity decoys,
and hybrid permeability + enzymatic cases. A few positive controls are included
so the split cannot be solved by over-abstaining.

Outputs:
    data/tasks/mechreason_hard.jsonl
    results/mechreason_hard_summary.json
    results/mechreason_hard_summary.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl, write_json, write_jsonl  # noqa: E402
from amr_bench.schema import validate_task  # noqa: E402

TASKS = ROOT / "data" / "tasks"
RESULTS = ROOT / "results"

OUT_JSONL = TASKS / "mechreason_hard.jsonl"
OUT_SUMMARY_JSON = RESULTS / "mechreason_hard_summary.json"
OUT_SUMMARY_MD = RESULTS / "mechreason_hard_summary.md"

TARGET_SIZE = 50


CATEGORY_NOTES = {
    "hypothesisgen_insufficient_evidence": (
        "Correct behavior is epistemic abstention: visible annotation evidence does not "
        "deterministically explain the AST phenotype."
    ),
    "intrinsic_acquired_ontology": (
        "Tests whether the model distinguishes chromosomal intrinsic mechanisms from "
        "acquired enzymatic mechanism labels."
    ),
    "regulator_lof_vs_direct_efflux": (
        "Tests regulator-loss causality rather than collapsing every derepressed efflux "
        "phenotype into generic efflux."
    ),
    "hybrid_porin_beta_lactamase": (
        "Tests primary/secondary mechanism reasoning for porin loss plus beta-lactamase "
        "co-drivers."
    ),
    "cefoxitin_substrate_decoy": (
        "Tempting beta-lactamase decoy: non-AmpC/non-carbapenemase beta-lactamases are "
        "visible, but cefoxitin resistance is assigned to porin loss."
    ),
    "drug_specificity_positive_control": (
        "Positive counterfactual for drug specificity: tet/oqx evidence can explain "
        "tetracycline, unlike paired tigecycline insufficiency cases."
    ),
    "cefoxitin_true_hydrolysis_control": (
        "Positive counterfactual for substrate specificity: AmpC/KPC/NDM/VIM-family "
        "enzymes can explain cefoxitin hydrolysis."
    ),
}


def main() -> None:
    tasks = read_jsonl(TASKS / "mechreason.jsonl")
    if not tasks:
        raise SystemExit("No MechReason tasks found. Run scripts/build_tasks.py first.")

    by_id = {task["task_id"]: task for task in tasks}
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    category_counts: Counter[str] = Counter()

    def add(task: dict[str, Any], category: str, rule: str, paired_task_id: str | None = None) -> None:
        if task["task_id"] in seen:
            return
        item = json.loads(json.dumps(task))
        hard_split = {
            "name": "mechreason_hard_50",
            "category": category,
            "selection_rule": rule,
            "rationale": CATEGORY_NOTES[category],
        }
        if paired_task_id:
            hard_split["paired_task_id"] = paired_task_id
        item["hard_split"] = hard_split
        selected.append(item)
        seen.add(task["task_id"])
        category_counts[category] += 1

    # 1. All HypothesisGen / insufficient-evidence cases.
    for task in sorted(tasks, key=task_id_sort_key):
        if task["gold"]["mechanism_class"] == "insufficient_evidence":
            add(task, "hypothesisgen_insufficient_evidence", "all insufficient_evidence MechReason tasks")

    # 2. All intrinsic ontology cases.
    for task in sorted(tasks, key=task_id_sort_key):
        if task["gold"]["mechanism_class"] == "intrinsic":
            add(task, "intrinsic_acquired_ontology", "all intrinsic MechReason tasks")

    # 3. All regulator LoF cases.
    for task in sorted(tasks, key=task_id_sort_key):
        if task["gold"]["mechanism_class"] == "regulator_loss_of_function":
            add(task, "regulator_lof_vs_direct_efflux", "all regulator_loss_of_function MechReason tasks")

    # 4. All explicitly tagged hybrid permeability cases.
    for task in sorted(tasks, key=task_id_sort_key):
        if task["gold"]["mechanism_class"] == "permeability_loss" and task["gold"].get("secondary_mechanism_classes"):
            add(task, "hybrid_porin_beta_lactamase", "all permeability_loss tasks with secondary_mechanism_classes")

    # 5. Ten cefoxitin decoys where visible beta-lactamases are not the primary gold mechanism.
    cefoxitin_decoys = [
        task
        for task in tasks
        if task["gold"]["mechanism_class"] == "permeability_loss"
        and task.get("antibiotic") == "cefoxitin"
        and not task["gold"].get("secondary_mechanism_classes")
    ]
    for task in sorted(cefoxitin_decoys, key=task_id_sort_key)[:10]:
        add(task, "cefoxitin_substrate_decoy", "first 10 non-hybrid cefoxitin permeability_loss tasks by task_id")

    # 6. Positive tetracycline controls paired to tigecycline insufficiency cases.
    # These keep the split contrastive: same family genes may be sufficient for
    # tetracycline while insufficient for tigecycline.
    paired_tetracycline_ids = ["mechreason_kp_000531", "mechreason_kp_000568", "mechreason_kp_000778", "mechreason_kp_000871"]
    paired_insufficient_ids = ["mechreason_kp_000532", "mechreason_kp_000569", "mechreason_kp_000779", "mechreason_kp_000872"]
    for task_id, paired_id in zip(paired_tetracycline_ids, paired_insufficient_ids, strict=True):
        add(
            by_id[task_id],
            "drug_specificity_positive_control",
            "manual deterministic mates for tigecycline insufficient_evidence cases",
            paired_task_id=paired_id,
        )

    # 7. Positive cefoxitin hydrolysis controls: one KPC, one NDM, one AmpC.
    for task_id, family in (
        ("mechreason_kp_000046", "KPC"),
        ("mechreason_kp_000258", "NDM"),
        ("mechreason_kp_000610", "CMY/AmpC"),
    ):
        add(
            by_id[task_id],
            "cefoxitin_true_hydrolysis_control",
            f"representative cefoxitin enzymatic_inactivation control with {family}",
        )

    if len(selected) != TARGET_SIZE:
        raise SystemExit(f"Expected {TARGET_SIZE} hard tasks, selected {len(selected)}")

    errors = validate_selected(selected)
    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors[:20]))

    selected.sort(key=lambda task: (task["hard_split"]["category"], task_id_sort_key(task)))
    write_jsonl(OUT_JSONL, selected)

    summary = build_summary(selected, tasks)
    write_json(OUT_SUMMARY_JSON, summary)
    OUT_SUMMARY_MD.write_text(render_summary_md(summary))

    print(f"Wrote {len(selected)} hard tasks -> {OUT_JSONL}")
    print(f"Wrote summary -> {OUT_SUMMARY_MD}")
    print(render_summary_md(summary))


def task_id_sort_key(task: dict[str, Any]) -> int:
    return int(str(task["task_id"]).rsplit("_", 1)[-1])


def validate_selected(tasks: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for task in tasks:
        task_errors = validate_task(task)
        for err in task_errors:
            errors.append(f"{task['task_id']}: {err}")
    return errors


def build_summary(selected: list[dict[str, Any]], full_tasks: list[dict[str, Any]]) -> dict[str, Any]:
    pilot_path = TASKS / "mechreason_pilot.jsonl"
    pilot_ids = {task["task_id"] for task in read_jsonl(pilot_path)} if pilot_path.exists() else set()

    category_counts = Counter(task["hard_split"]["category"] for task in selected)
    class_counts = Counter(task["gold"]["mechanism_class"] for task in selected)
    antibiotic_counts = Counter(task.get("antibiotic", "?") for task in selected)
    phenotype_counts = Counter(task["gold"].get("phenotype", "?") for task in selected)
    overlap_with_pilot = sorted(task["task_id"] for task in selected if task["task_id"] in pilot_ids)

    by_category: dict[str, list[str]] = defaultdict(list)
    for task in selected:
        by_category[task["hard_split"]["category"]].append(task["task_id"])

    return {
        "split_name": "mechreason_hard_50",
        "n_tasks": len(selected),
        "source": "data/tasks/mechreason.jsonl",
        "selection": "deterministic hard-category split from existing MechReason tasks",
        "full_mechreason_task_count": len(full_tasks),
        "category_counts": dict(sorted(category_counts.items())),
        "mechanism_class_counts": dict(sorted(class_counts.items())),
        "antibiotic_counts": dict(sorted(antibiotic_counts.items())),
        "phenotype_counts": dict(sorted(phenotype_counts.items())),
        "overlap_with_mechreason_pilot_count": len(overlap_with_pilot),
        "overlap_with_mechreason_pilot_task_ids": overlap_with_pilot,
        "task_ids_by_category": {k: v for k, v in sorted(by_category.items())},
    }


def render_summary_md(summary: dict[str, Any]) -> str:
    lines = [
        "# MechReason Hard Split Summary",
        "",
        f"- Split: `{summary['split_name']}`",
        f"- Tasks: {summary['n_tasks']}",
        f"- Source: `{summary['source']}`",
        f"- Selection: {summary['selection']}",
        f"- Overlap with original 50-task pilot: {summary['overlap_with_mechreason_pilot_count']} tasks",
        "",
        "## Category Counts",
        "",
        "| Category | n |",
        "| --- | ---: |",
    ]
    for category, count in summary["category_counts"].items():
        lines.append(f"| `{category}` | {count} |")

    lines += [
        "",
        "## Mechanism Class Counts",
        "",
        "| Mechanism class | n |",
        "| --- | ---: |",
    ]
    for mechanism_class, count in summary["mechanism_class_counts"].items():
        lines.append(f"| `{mechanism_class}` | {count} |")

    lines += [
        "",
        "## Antibiotic Counts",
        "",
        "| Antibiotic | n |",
        "| --- | ---: |",
    ]
    for antibiotic, count in summary["antibiotic_counts"].items():
        lines.append(f"| {antibiotic} | {count} |")

    lines += [
        "",
        "## Task IDs By Category",
        "",
    ]
    for category, task_ids in summary["task_ids_by_category"].items():
        lines.append(f"### `{category}`")
        lines.append("")
        lines.append(", ".join(f"`{task_id}`" for task_id in task_ids))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    main()
