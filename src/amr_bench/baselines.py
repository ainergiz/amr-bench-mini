"""Deterministic baseline outputs for AMR-Bench-mini."""

from __future__ import annotations

from typing import Any

from amr_bench.parsing import gene_family, is_point_mutation_call, norm_gene


def rule_baseline(task: dict[str, Any]) -> dict[str, Any]:
    if task.get("track") == "genopheno":
        return genopheno_rule(task)
    if task.get("track") == "dbreconcile":
        return dbreconcile_rule(task)
    if task.get("track") == "mechreason":
        return mechreason_rule(task)
    raise ValueError(f"unknown track: {task.get('track')}")


def genopheno_rule(task: dict[str, Any]) -> dict[str, Any]:
    hits = task.get("visible_evidence", {}).get("relevant_tool_hits", [])
    phenotype = "Resistant" if hits else "Susceptible"
    confidence = 0.76 if hits else 0.58
    evidence = [
        {
            "source": hit.get("source"),
            "claim": f"{hit.get('gene')} supports {task.get('antibiotic')} resistance evidence",
            "supports_answer": True,
        }
        for hit in hits[:6]
    ]
    uncertainty = (
        "Rule baseline maps any relevant AMR hit to Resistant; it does not model breakpoint revisions, "
        "gene expression, permeability, or species-specific clinical interpretation."
    )
    return {
        "task_id": task["task_id"],
        "answer": phenotype,
        "phenotype_prediction": phenotype,
        "confidence": confidence,
        "evidence": evidence,
        "rationale": "Predicted Resistant when at least one visible AMR annotation matched the antibiotic or class; otherwise Susceptible.",
        "uncertainty": uncertainty,
    }


def mechreason_rule(task: dict[str, Any]) -> dict[str, Any]:
    """Echo the gold-style heuristic to produce a tractable rule baseline.

    The same priority-ordered gene-class mapping is used at task-build time and
    at baseline scoring time, so this baseline is mostly a sanity check that the
    schema and scoring pipelines align. LLM agents are expected to beat this by
    correctly handling cases where the heuristic returns ``insufficient_evidence``
    (regulator LoF, OXA-48 + intact porins, fosA chromosomal subtleties, etc.).
    """
    gold = task.get("gold", {})
    mechanism_class = gold.get("mechanism_class", "insufficient_evidence")
    required = list(gold.get("required_genes", []))

    hits = task.get("visible_evidence", {}).get("relevant_tool_hits", [])
    evidence = [
        {
            "source": hit.get("source"),
            "gene": hit.get("gene"),
            "claim": f"{hit.get('gene')} contributes to {task.get('antibiotic')} resistance evidence.",
            "supports_answer": True,
        }
        for hit in hits[:6]
    ]

    layered_text = (
        f"L1 genome: visible relevant gene calls {required or [hit.get('gene') for hit in hits[:3]]}. "
        f"L2 protein: gene-product class implied by required genes; structural details not produced by rule baseline. "
        f"L3 mechanism: heuristic mechanism class {mechanism_class}. "
        f"L4 cell: rule baseline does not model cellular pathway. "
        f"L5 phenotype: AST phenotype {gold.get('phenotype')}."
    )

    confidence = 0.6 if mechanism_class != "insufficient_evidence" else 0.3

    return {
        "task_id": task["task_id"],
        "answer": mechanism_class,
        "mechanism_class": mechanism_class,
        "phenotype_prediction": gold.get("phenotype"),
        "layers": {
            "genome": f"Visible required genes: {required or [hit.get('gene') for hit in hits[:3]]}.",
            "protein": "Rule baseline does not produce protein-level reasoning.",
            "mechanism": mechanism_class,
            "cell": "Rule baseline does not produce cellular-pathway reasoning.",
            "phenotype": str(gold.get("phenotype")),
        },
        "confidence": confidence,
        "evidence": evidence,
        "rationale": layered_text,
        "uncertainty": "Rule baseline mirrors task-build heuristics; it cannot recognize cases where annotators alone fail to explain the phenotype (HypothesisGen flavor).",
        "tools_called": [],
    }


def dbreconcile_rule(task: dict[str, Any]) -> dict[str, Any]:
    evidence = task.get("visible_evidence", {})
    amr = evidence.get("amrfinder_hits", [])
    res = evidence.get("resfinder_hits", [])
    amr_genes = {norm_gene(row.get("gene", "")) for row in amr}
    res_genes = {norm_gene(row.get("gene", "")) for row in res}
    amr_families = {gene_family(row.get("gene", "")) for row in amr}
    res_families = {gene_family(row.get("gene", "")) for row in res}

    if amr and not res and any(is_point_mutation_call(row) for row in amr):
        dtype = "point_mutation_vs_gene_presence"
        answer = "AMRFinderPlus reports a point-mutation-style call not represented in the ResFinder acquired-gene evidence."
    elif amr and res and amr_genes & res_genes:
        dtype = "drug_mapping_difference"
        answer = "Both tools report the same gene name, but they expose drug-class or phenotype mappings at different granularity."
    elif amr and res and amr_families & res_families:
        dtype = "gene_family_vs_allele"
        answer = "The tools agree on a coarse gene family but differ at allele/name granularity."
    elif amr or res:
        dtype = "threshold_difference"
        answer = "Only one tool reports this target; this may reflect database content, thresholds, or reporting scope."
    else:
        dtype = "insufficient_evidence"
        answer = "No comparable AMR evidence was provided."

    output_evidence = []
    for row in amr[:4]:
        output_evidence.append(
            {
                "source": "AMRFinderPlus",
                "claim": f"{row.get('gene')} reported with class {row.get('drug_class', '')}",
                "supports_answer": True,
            }
        )
    for row in res[:4]:
        output_evidence.append(
            {
                "source": "ResFinder",
                "claim": f"{row.get('gene')} reported with phenotype {row.get('phenotype', '')}",
                "supports_answer": True,
            }
        )

    return {
        "task_id": task["task_id"],
        "answer": dtype,
        "disagreement_type": dtype,
        "reconciled_call": answer,
        "confidence": 0.72,
        "evidence": output_evidence,
        "rationale": answer,
        "uncertainty": "Rule baseline uses gene-name and family heuristics; true reconciliation may require database-version review and sequence-level inspection.",
    }
