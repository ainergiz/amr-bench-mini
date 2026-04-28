#!/usr/bin/env python3
"""Build the paper headline table from existing run summaries.

Reads each model's pilot + hard run from results/llm_eval/ (using the rescore
artifacts produced by scripts/rescore_runs.py), computes Wilson 95% CIs for
subgroups with n >= 10, and reports rare subgroups (n < 10) descriptively.

Outputs:
    results/headline_table.md
    results/headline_table.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl, write_json  # noqa: E402
from amr_bench.scoring import score_output  # noqa: E402

LLM_EVAL = ROOT / "results" / "llm_eval"
TASKS = ROOT / "data" / "tasks"
OUT_MD = ROOT / "results" / "headline_table.md"
OUT_JSON = ROOT / "results" / "headline_table.json"

CI_MIN_N = 10  # Wilson CIs only when subgroup n >= this threshold.
Z_95 = 1.959963984540054  # 1 - alpha/2 for alpha=0.05.

# (Display name, run dir name)
PILOT_RUNS = [
    ("GPT-5.4", "pilot_gpt-5.4_20260425T193051Z"),
    ("Gemini 3.1 Pro", "pilot_gemini-3.1-pro-preview_20260425T223711Z"),
    ("Claude Opus 4.7", "pilot_batch_claude-opus-4-7_20260426T083024Z"),
]
HARD_RUNS = [
    ("GPT-5.4", "hard_gpt-5.4_20260426Tmanual"),
    ("Gemini 3.1 Pro", "hard_gemini-3.1-pro-preview_20260426Tmanual"),
    ("Claude Opus 4.7", "hard_batch_claude-opus-4-7_20260426Tmanual"),
]


def wilson_ci(k: int, n: int, z: float = Z_95) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    z2 = z * z
    denom = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n))) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def fmt_pct(p: float) -> str:
    return f"{p * 100:.1f}%"


def fmt_acc(k: int, n: int, with_ci: bool = True) -> str:
    if n == 0:
        return "—"
    p = k / n
    if not with_ci or n < CI_MIN_N:
        return f"{fmt_pct(p)} ({k}/{n})"
    lo, hi = wilson_ci(k, n)
    return f"{fmt_pct(p)} [{fmt_pct(lo)}, {fmt_pct(hi)}] ({k}/{n})"


def score_run(run_dir: Path, gold_idx: dict, group_key) -> dict:
    """Run scoring against gold_idx; return overall + per-group counts."""
    rows = read_jsonl(run_dir / "raw_outputs.jsonl")
    overall_n = overall_k = 0
    by_group: dict[str, dict[str, int]] = {}
    for row in rows:
        tid = row["task_id"]
        task = gold_idx.get(tid)
        if not task:
            continue
        s = score_output(task, row.get("output") or {})
        overall_n += 1
        if s.get("correct"):
            overall_k += 1
        g = group_key(task)
        if g is None:
            continue
        bucket = by_group.setdefault(g, {"n": 0, "k": 0, "mech_correct": 0})
        bucket["n"] += 1
        if s.get("correct"):
            bucket["k"] += 1
        if s.get("mechanism_class_correct"):
            bucket["mech_correct"] += 1
    return {"n": overall_n, "k": overall_k, "by_group": by_group}


def collect_split(runs: list[tuple[str, str]], gold_idx: dict, group_key) -> dict:
    out = {}
    for label, run_name in runs:
        run_dir = LLM_EVAL / run_name
        if not run_dir.exists():
            print(f"  [warn] missing run dir: {run_dir}")
            continue
        out[label] = score_run(run_dir, gold_idx, group_key)
    return out


def render_headline(strict_pilot, adj_pilot, strict_hard, adj_hard) -> str:
    lines = [
        "# Headline Table — Strict and Audit-Adjudicated Accuracy",
        "",
        "All accuracies report Wilson 95% CIs when subgroup *n* ≥ 10. Rare subgroups "
        "(*n* < 10) report point estimates only and are not used for population claims.",
        "",
        "Strict gold = pre-adjudication heuristic labels (`data/tasks/mechreason_strict.jsonl`).  ",
        "Adjudicated gold = post-audit labels with the four invariant overrides "
        "(3× *fosA* `intrinsic` → `enzymatic_inactivation`; 1× ArmA hybrid "
        "`enzymatic_inactivation` → `target_modification` + secondary `enzymatic_inactivation`) "
        "(`data/tasks/mechreason.jsonl`).",
        "",
        "## Overall composite accuracy",
        "",
        "| Split | Model | Strict accuracy | Adjudicated accuracy |",
        "| --- | --- | --- | --- |",
    ]
    for label in [m for m, _ in PILOT_RUNS]:
        s = strict_pilot.get(label, {"n": 0, "k": 0})
        a = adj_pilot.get(label, {"n": 0, "k": 0})
        lines.append(
            f"| Balanced pilot (n=50) | {label} | {fmt_acc(s['k'], s['n'])} | {fmt_acc(a['k'], a['n'])} |"
        )
    for label in [m for m, _ in HARD_RUNS]:
        s = strict_hard.get(label, {"n": 0, "k": 0})
        a = adj_hard.get(label, {"n": 0, "k": 0})
        lines.append(
            f"| Hard diagnostic (n=50) | {label} | {fmt_acc(s['k'], s['n'])} | {fmt_acc(a['k'], a['n'])} |"
        )

    lines += [
        "",
        "## Hard split — per-category accuracy (adjudicated gold)",
        "",
        "Per-category Wilson CIs are reported for `hypothesisgen_insufficient_evidence` "
        f"and `cefoxitin_substrate_decoy` only (n ≥ {CI_MIN_N}). The other five "
        "categories provide contrastive controls and ontology stress tests; their "
        "accuracies are reported as point estimates and are not used for population "
        "claims.",
        "",
        "| Category | n | GPT-5.4 | Gemini 3.1 Pro | Claude Opus 4.7 |",
        "| --- | ---: | --- | --- | --- |",
    ]

    categories: list[tuple[str, int]] = []
    seen: set[str] = set()
    for label in adj_hard:
        for cat, bucket in adj_hard[label]["by_group"].items():
            if cat not in seen:
                categories.append((cat, bucket["n"]))
                seen.add(cat)
    categories.sort(key=lambda x: -x[1])

    for cat, n in categories:
        cells = []
        for label in [m for m, _ in HARD_RUNS]:
            bucket = adj_hard.get(label, {"by_group": {}})["by_group"].get(cat, {"n": 0, "k": 0})
            cells.append(fmt_acc(bucket["k"], bucket["n"]))
        lines.append(f"| `{cat}` | {n} | " + " | ".join(cells) + " |")

    lines += [
        "",
        "## Pilot split — per-class accuracy (adjudicated gold)",
        "",
        "Per-class CIs are reported only where pilot subgroup n ≥ 10.",
        "",
        "| Class | n | GPT-5.4 | Gemini 3.1 Pro | Claude Opus 4.7 |",
        "| --- | ---: | --- | --- | --- |",
    ]

    pilot_classes: list[tuple[str, int]] = []
    seen2: set[str] = set()
    for label in adj_pilot:
        for cls, bucket in adj_pilot[label]["by_group"].items():
            if cls not in seen2:
                pilot_classes.append((cls, bucket["n"]))
                seen2.add(cls)
    pilot_classes.sort(key=lambda x: -x[1])

    for cls, n in pilot_classes:
        cells = []
        for label in [m for m, _ in PILOT_RUNS]:
            bucket = adj_pilot.get(label, {"by_group": {}})["by_group"].get(cls, {"n": 0, "k": 0})
            cells.append(fmt_acc(bucket["k"], bucket["n"]))
        lines.append(f"| `{cls}` | {n} | " + " | ".join(cells) + " |")

    lines += [
        "",
        "## Rare-class strategy",
        "",
        "We report Wilson 95% CIs only when subgroup *n* ≥ "
        f"{CI_MIN_N}. Below this threshold, point estimates are reported descriptively "
        "without intervals to avoid implying population precision that the data do "
        "not support. Rare-class members in this benchmark are:",
        "",
        "- `intrinsic` (n=3 in pilot, 3 in hard) — three *fosA* tasks; reported under "
        "`intrinsic_acquired_ontology` to expose the strict-vs-adjudicated gap.",
        "- `regulator_loss_of_function` (n=2 in pilot, 2 in hard) — diagnostic "
        "controls for regulator-vs-direct-efflux causality.",
        "- `cefoxitin_true_hydrolysis_control` (n=3 hard only), "
        "`drug_specificity_positive_control` (n=4 hard only), "
        "`hybrid_porin_beta_lactamase` (n=4 hard only) — contrastive controls; "
        "all three are passed by all three models in the current adjudicated runs.",
        "",
        "We do **not** collapse rare classes into a generic `rare-mechanism` bucket "
        "because the categories are diagnostic of distinct reasoning failures "
        "(ontology vs. causality vs. hybrid mechanisms). Pooling would obscure the "
        "exact failure mode the split was constructed to expose.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    strict_full = {t["task_id"]: t for t in read_jsonl(TASKS / "mechreason_strict.jsonl")}
    adjusted_full = {t["task_id"]: t for t in read_jsonl(TASKS / "mechreason.jsonl")}

    pilot_ids = [t["task_id"] for t in read_jsonl(TASKS / "mechreason_pilot.jsonl")]
    hard_ids = [t["task_id"] for t in read_jsonl(TASKS / "mechreason_hard.jsonl")]

    strict_pilot_idx = {tid: strict_full[tid] for tid in pilot_ids if tid in strict_full}
    strict_hard_idx = {tid: strict_full[tid] for tid in hard_ids if tid in strict_full}
    adj_pilot_idx = {tid: adjusted_full[tid] for tid in pilot_ids if tid in adjusted_full}
    adj_hard_idx = {tid: adjusted_full[tid] for tid in hard_ids if tid in adjusted_full}

    # Hard tasks carry hard_split.category; pull it from the hard split file (which
    # has post-adjudication golds + frozen split metadata).
    hard_meta = {t["task_id"]: t.get("hard_split", {}).get("category") for t in read_jsonl(TASKS / "mechreason_hard.jsonl")}

    def hard_group_key(task: dict) -> str | None:
        return hard_meta.get(task["task_id"])

    def pilot_group_key(task: dict) -> str:
        return task["gold"]["mechanism_class"]

    print("Pilot — strict")
    strict_pilot = collect_split(PILOT_RUNS, strict_pilot_idx, pilot_group_key)
    print("Pilot — adjusted")
    adj_pilot = collect_split(PILOT_RUNS, adj_pilot_idx, pilot_group_key)
    print("Hard — strict")
    strict_hard = collect_split(HARD_RUNS, strict_hard_idx, hard_group_key)
    print("Hard — adjusted")
    adj_hard = collect_split(HARD_RUNS, adj_hard_idx, hard_group_key)

    md = render_headline(strict_pilot, adj_pilot, strict_hard, adj_hard)
    OUT_MD.write_text(md)
    write_json(OUT_JSON, {
        "pilot_strict": strict_pilot,
        "pilot_adjusted": adj_pilot,
        "hard_strict": strict_hard,
        "hard_adjusted": adj_hard,
        "ci_min_n": CI_MIN_N,
    })
    print(f"\nWrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
