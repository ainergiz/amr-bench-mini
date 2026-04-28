#!/usr/bin/env python3
"""Stratified audit of MechReason gold labels for biological credibility.

The MechReason `gold.mechanism_class` is derived heuristically by
`scripts/build_tasks.py::infer_mechanism()` — a priority-ordered map from
gene/variant/method evidence to mechanism class. Before the benchmark is
treated as ground truth, the heuristic must be audited by a microbiologist.

This script renders a stratified sample of MechReason tasks (with extra
weight on permeability_loss, regulator_loss_of_function, and
insufficient_evidence per the spike-failure-mode taxonomy) into:

  results/mechreason_audit/audit_pack.md   - human-readable case cards
  results/mechreason_audit/audit_form.tsv  - structured input grid for the auditor

Auditor workflow:

  1. Open audit_pack.md, read each card alongside audit_form.tsv.
  2. For each task, mark `gold_class_decision` (KEEP / OVERRIDE / AMBIGUOUS),
     `gold_class_proposed` (one of VALID_MECHANISM_CLASSES), and free-text notes.
  3. Optionally mark `required_genes_decision` similarly.
  4. Run scripts/apply_audit_overrides.py to rebuild MechReason gold from the
     filled audit_form.tsv (only when audit is complete).
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl  # noqa: E402
from amr_bench.schema import VALID_MECHANISM_CLASSES  # noqa: E402

RESULTS = ROOT / "results"
DATA = ROOT / "data"
TASKS = DATA / "tasks"
OUT_DIR = RESULTS / "mechreason_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Stratification weights — give priority to the spike's high-value failure-mode
# subtleties. These are the gold-label categories most likely to be miscalled by
# the heuristic and most consequential for the paper.
STRATIFIED_TARGETS: dict[str, int] = {
    "insufficient_evidence": 6,
    "regulator_loss_of_function": 5,
    "permeability_loss": 6,
    "intrinsic": 1,
    "target_modification": 4,
    "efflux": 3,
    "metabolic_bypass": 3,
    "enzymatic_inactivation": 4,
    "target_protection": 0,
}

AUDIT_FIELDS = [
    "task_id",
    "antibiotic",
    "phenotype",
    "gold_class",
    "gold_required_genes",
    "gold_class_decision",      # KEEP / OVERRIDE / AMBIGUOUS
    "gold_class_proposed",      # if OVERRIDE: a value in VALID_MECHANISM_CLASSES
    "required_genes_decision",  # KEEP / OVERRIDE / AMBIGUOUS
    "required_genes_proposed",  # comma-separated
    # Optional hybrid-mechanism fields. Populate for AMBIGUOUS cases where two
    # mechanisms genuinely co-drive resistance (e.g., ESBL hyperexpression +
    # porin loss → carbapenem R). Leave blank for single-mechanism cases.
    "secondary_classes_proposed",  # comma-separated; subset of VALID_MECHANISM_CLASSES
    "interaction_type_proposed",   # additive / synergistic / uncertain
    "auditor_notes",
]


def main() -> None:
    tasks = read_jsonl(TASKS / "mechreason.jsonl")
    if not tasks:
        raise SystemExit("No MechReason tasks found. Run scripts/build_tasks.py first.")

    by_class: dict[str, list[dict]] = defaultdict(list)
    for t in tasks:
        by_class[t["gold"]["mechanism_class"]].append(t)

    rng = random.Random(20260425)  # deterministic stratified sample
    sampled: list[dict] = []
    for cls, target in STRATIFIED_TARGETS.items():
        pool = by_class.get(cls, [])
        if not pool or target == 0:
            continue
        take = min(target, len(pool))
        sampled.extend(rng.sample(pool, take))

    sampled.sort(key=lambda t: (t["gold"]["mechanism_class"], t["task_id"]))

    write_audit_pack(sampled)
    write_audit_form(sampled)
    write_meta(sampled, by_class)

    print(f"Audit corpus size: {len(tasks)} MechReason tasks")
    for cls in sorted(STRATIFIED_TARGETS):
        avail = len(by_class.get(cls, []))
        target = STRATIFIED_TARGETS[cls]
        taken = sum(1 for t in sampled if t["gold"]["mechanism_class"] == cls)
        print(f"  {cls:32s} target={target:>2}  available={avail:>3}  sampled={taken}")
    print(f"\nWrote {OUT_DIR / 'audit_pack.md'}")
    print(f"Wrote {OUT_DIR / 'audit_form.tsv'}")
    print(f"Wrote {OUT_DIR / 'audit_meta.json'}")


def write_audit_pack(tasks: list[dict]) -> None:
    lines: list[str] = [
        "# MechReason Label Audit — stratified sample",
        "",
        f"This pack contains {len(tasks)} MechReason cases sampled across mechanism classes "
        "(weighted toward `permeability_loss`, `regulator_loss_of_function`, and "
        "`insufficient_evidence` — the categories most likely to be miscalled by the "
        "heuristic). Each card shows the task input as the agent sees it, plus the "
        "heuristic-derived gold for auditor review.",
        "",
        "Mark decisions in `audit_form.tsv` (one row per task here). Valid mechanism "
        f"classes: `{', '.join(sorted(VALID_MECHANISM_CLASSES))}`.",
        "",
        "---",
        "",
    ]
    for idx, task in enumerate(tasks, 1):
        lines.append(f"## {idx}. {task['task_id']}  ·  `{task['gold']['mechanism_class']}`")
        lines.append("")
        lines.append(f"- **Genome**: {task['genome_name']} ({task['genome_id']})")
        meta = task.get("metadata") or {}
        meta_bits = [f"{k}: {v}" for k, v in meta.items() if v not in (None, "", 0)]
        if meta_bits:
            lines.append(f"- **Metadata**: {' · '.join(meta_bits[:6])}")
        lines.append(f"- **Antibiotic**: `{task['antibiotic']}` (class: {task['antibiotic_class']})")
        lines.append(f"- **AST phenotype**: `{task['gold']['phenotype']}`")
        lines.append("")
        lines.append("**Visible annotator hits the agent gets to see:**")
        lines.append("")
        hits = task.get("visible_evidence", {}).get("relevant_tool_hits", [])
        if hits:
            lines.append("| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |")
            lines.append("| --- | --- | --- | --- | --- |")
            for h in hits:
                src = h.get("source", "")
                gene = h.get("gene", "")
                if src == "AMRFinderPlus":
                    detail = f"{h.get('drug_class','')} / {h.get('subclass','')}"
                elif src == "ResFinder":
                    detail = (h.get("phenotype") or "")[:80]
                else:
                    detail = ""
                ident = h.get("identity")
                cov = h.get("coverage")
                ic = f"{ident:.1f}% / {cov:.1f}%" if isinstance(ident, (int, float)) and isinstance(cov, (int, float)) else ""
                method = h.get("method", "")
                lines.append(f"| {src} | `{gene}` | {detail} | {ic} | {method} |")
        else:
            lines.append("*(no relevant tool hits for this drug — HypothesisGen flavor)*")
        lines.append("")
        lines.append(
            f"**Heuristic gold:** `{task['gold']['mechanism_class']}` · "
            f"required_genes={task['gold']['required_genes']}"
        )
        lines.append("")
        lines.append(f"> _Heuristic rationale:_ {task['gold']['rationale']}")
        lines.append("")
        full_amr = task.get("visible_evidence", {}).get("all_amrfinder_hit_count", 0)
        full_res = task.get("visible_evidence", {}).get("all_resfinder_hit_count", 0)
        lines.append(
            f"_Coverage context: agent saw {len(hits)} drug-relevant hits; "
            f"the underlying isolate has {full_amr} total AMRFinder + {full_res} total ResFinder hits._"
        )
        lines.append("")
        lines.append("---")
        lines.append("")
    (OUT_DIR / "audit_pack.md").write_text("\n".join(lines))


def write_audit_form(tasks: list[dict]) -> None:
    out = OUT_DIR / "audit_form.tsv"
    with out.open("w", newline="") as h:
        writer = csv.DictWriter(h, fieldnames=AUDIT_FIELDS, delimiter="\t")
        writer.writeheader()
        for task in tasks:
            writer.writerow({
                "task_id": task["task_id"],
                "antibiotic": task["antibiotic"],
                "phenotype": task["gold"]["phenotype"],
                "gold_class": task["gold"]["mechanism_class"],
                "gold_required_genes": ",".join(task["gold"]["required_genes"]),
                "gold_class_decision": "",
                "gold_class_proposed": "",
                "required_genes_decision": "",
                "required_genes_proposed": "",
                "secondary_classes_proposed": "",
                "interaction_type_proposed": "",
                "auditor_notes": "",
            })


def write_meta(tasks: list[dict], by_class: dict[str, list]) -> None:
    meta = {
        "audit_size": len(tasks),
        "stratified_targets": STRATIFIED_TARGETS,
        "available_per_class": {cls: len(rows) for cls, rows in by_class.items()},
        "sampled_per_class": {
            cls: sum(1 for t in tasks if t["gold"]["mechanism_class"] == cls)
            for cls in sorted(STRATIFIED_TARGETS)
        },
        "instructions_for_auditor": [
            "Read audit_pack.md card-by-card, alongside audit_form.tsv (one row per card).",
            "For each task, set gold_class_decision to KEEP, OVERRIDE, or AMBIGUOUS.",
            "If OVERRIDE: set gold_class_proposed to one of: " + ", ".join(sorted(VALID_MECHANISM_CLASSES)),
            "Do the same for required_genes_decision/proposed if needed.",
            "Add free-text notes capturing the biological reasoning, esp. for AMBIGUOUS / OVERRIDE rows.",
            "When done, run scripts/apply_audit_overrides.py to rebuild MechReason gold.",
        ],
    }
    (OUT_DIR / "audit_meta.json").write_text(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
