#!/usr/bin/env python3
"""Compare two model runs on the same task subset task-by-task.

Used to compare the tool-augmented Gemini hard run against the no-tool baseline.
Reports: per-category accuracy delta, overall flips, and the specific task IDs
that changed correctness.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl  # noqa: E402
from amr_bench.scoring import score_output  # noqa: E402

LLM_EVAL = ROOT / "results" / "llm_eval"
TASKS = ROOT / "data" / "tasks"

BASELINE = "hard_gemini-3.1-pro-preview_20260426Tmanual"
TOOL = "hard_tool_gemini-3.1-pro-preview_20260426T112234Z"
OUT_MD = ROOT / "results" / "tool_vs_baseline_gemini_hard.md"


def score_run(run_name: str, gold_idx: dict) -> dict[str, dict]:
    rows = read_jsonl(LLM_EVAL / run_name / "raw_outputs.jsonl")
    out = {}
    for r in rows:
        tid = r["task_id"]
        task = gold_idx.get(tid)
        if not task:
            continue
        s = score_output(task, r.get("output") or {})
        out[tid] = {
            "correct": bool(s.get("correct")),
            "mech_correct": bool(s.get("mechanism_class_correct")),
            "prediction": s.get("prediction"),
        }
    return out


def main() -> None:
    adjusted_gold = {t["task_id"]: t for t in read_jsonl(TASKS / "mechreason.jsonl")}
    hard = read_jsonl(TASKS / "mechreason_hard.jsonl")
    hard_idx = {t["task_id"]: t for t in hard}
    category = {tid: t.get("hard_split", {}).get("category") for tid, t in hard_idx.items()}

    base = score_run(BASELINE, adjusted_gold)
    tool = score_run(TOOL, adjusted_gold)

    by_cat: dict[str, dict] = defaultdict(lambda: {"n": 0, "base_k": 0, "tool_k": 0, "flips_pos": [], "flips_neg": []})
    for tid in base:
        if tid not in tool:
            continue
        cat = category.get(tid, "?")
        c = by_cat[cat]
        c["n"] += 1
        if base[tid]["correct"]:
            c["base_k"] += 1
        if tool[tid]["correct"]:
            c["tool_k"] += 1
        if base[tid]["correct"] != tool[tid]["correct"]:
            entry = {
                "task_id": tid,
                "antibiotic": hard_idx[tid].get("antibiotic"),
                "gold": adjusted_gold[tid]["gold"]["mechanism_class"],
                "base_pred": base[tid]["prediction"],
                "tool_pred": tool[tid]["prediction"],
            }
            (c["flips_pos"] if tool[tid]["correct"] else c["flips_neg"]).append(entry)

    base_total = sum(v["base_k"] for v in by_cat.values())
    tool_total = sum(v["tool_k"] for v in by_cat.values())
    n_total = sum(v["n"] for v in by_cat.values())

    lines = [
        "# Tool intervention vs no-tool — Gemini 3.1 Pro on hard split",
        "",
        f"- Baseline run: `{BASELINE}` (no tool)",
        f"- Tool-augmented run: `{TOOL}` (CARD ARO substrate context pre-resolved per visible gene)",
        "- Scoring: adjudicated gold (`data/tasks/mechreason.jsonl`)",
        f"- N tasks: {n_total}",
        "",
        "## Headline",
        "",
        f"- Baseline accuracy: **{base_total}/{n_total} = {base_total/n_total*100:.1f}%**",
        f"- Tool-augmented accuracy: **{tool_total}/{n_total} = {tool_total/n_total*100:.1f}%**",
        f"- Net delta: **{tool_total - base_total:+d}** tasks",
        "",
        "## Per-category breakdown",
        "",
        "| Category | n | Baseline | Tool-augmented | Δ |",
        "| --- | ---: | --- | --- | ---: |",
    ]
    for cat in sorted(by_cat, key=lambda c: -by_cat[c]["n"]):
        v = by_cat[cat]
        delta = v["tool_k"] - v["base_k"]
        lines.append(
            f"| `{cat}` | {v['n']} | {v['base_k']}/{v['n']} ({v['base_k']/v['n']*100:.0f}%) | "
            f"{v['tool_k']}/{v['n']} ({v['tool_k']/v['n']*100:.0f}%) | {delta:+d} |"
        )

    pos_flips = [f for v in by_cat.values() for f in v["flips_pos"]]
    neg_flips = [f for v in by_cat.values() for f in v["flips_neg"]]

    lines += [
        "",
        f"## Tasks gained by tool ({len(pos_flips)})",
        "",
    ]
    if pos_flips:
        lines.append("| task_id | antibiotic | gold | baseline pred | tool pred |")
        lines.append("| --- | --- | --- | --- | --- |")
        for f in pos_flips:
            lines.append(
                f"| `{f['task_id']}` | {f['antibiotic']} | `{f['gold']}` | `{f['base_pred']}` | `{f['tool_pred']}` |"
            )
    else:
        lines.append("*None.*")

    lines += [
        "",
        f"## Tasks lost by tool ({len(neg_flips)})",
        "",
    ]
    if neg_flips:
        lines.append("| task_id | antibiotic | gold | baseline pred | tool pred |")
        lines.append("| --- | --- | --- | --- | --- |")
        for f in neg_flips:
            lines.append(
                f"| `{f['task_id']}` | {f['antibiotic']} | `{f['gold']}` | `{f['base_pred']}` | `{f['tool_pred']}` |"
            )
    else:
        lines.append("*None.*")

    lines += [
        "",
        "## Interpretation",
        "",
        "The CARD substrate context block injects, for every visible AMRFinderPlus / "
        "ResFinder hit, the canonical drug-class coverage and resistance mechanism "
        "from CARD ARO. The intent of the experiment is to test whether the central "
        "abstention failure (`hypothesisgen_insufficient_evidence`) is a "
        "knowledge-retrieval gap that pre-resolved substrate biology can close, or a "
        "calibration failure that survives even when the substrate facts are stated "
        "explicitly in the prompt.",
        "",
        "Gemini 3.1 Pro was already at 100% on `cefoxitin_substrate_decoy` without "
        "tools, so this category cannot test the substrate-knowledge hypothesis on "
        "Gemini specifically — there is no headroom. The relevant signal is the "
        "`hypothesisgen_insufficient_evidence` row.",
        "",
        "### Headline finding",
        "",
        "Net effect on the abstention category is **+1/24 (4.2pp)**: well inside the "
        "Wilson 95% CI for either run and indistinguishable from noise. Aggregate "
        "accuracy is **identical** at 32/50 because the tool gained two cases on "
        "`hypothesisgen_insufficient_evidence` while losing two cases — one on "
        "`drug_specificity_positive_control` and one on the same "
        "`hypothesisgen_insufficient_evidence` category. ",
        "",
        "### Asymmetric flips",
        "",
        "The two losses are diagnostic. On `mechreason_kp_000778` (tetracycline + "
        "*tet(A)* + *oqxAB*, gold `efflux`), the no-tool model correctly invoked "
        "efflux; with substrate context the model abstained, apparently because the "
        "CARD card for *oqxA/B* lists glycylcyclines and tigecycline alongside "
        "tetracycline coverage and the model became conservative about the call. On "
        "`mechreason_kp_000569` (tigecycline, gold `insufficient_evidence`), the no-"
        "tool model correctly abstained; with substrate context the model called "
        "`efflux`, presumably anchoring on the same broad CARD substrate listing.",
        "",
        "Substrate context, in other words, is *bidirectionally* persuasive: it "
        "encourages the model to invoke a mechanism when the visible gene's CARD "
        "card mentions the queried drug class, regardless of whether the visible "
        "evidence is mechanistically sufficient. This is the opposite of the "
        "calibration property the abstention category requires.",
        "",
        "### Implication for the paper",
        "",
        "Pre-resolved substrate retrieval does not fix the central abstention "
        "failure on Gemini 3.1 Pro. The four-percentage-point gain on "
        "`hypothesisgen_insufficient_evidence` is offset one-for-one by losses on "
        "neighboring categories. This supports the framing that the abstention "
        "failure is a *calibration* problem, not a *retrieval-only* problem: adding "
        "substrate-coverage facts to the prompt does not make the model reliably "
        "recognize that visible evidence is insufficient. The paper's claim should "
        "be narrower: CARD substrate context alone is not sufficient for "
        "evidence-sufficiency reasoning in this prompt-only setting.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines))
    print(f"Wrote {OUT_MD}")
    print()
    print("\n".join(lines[6:18]))


if __name__ == "__main__":
    main()
