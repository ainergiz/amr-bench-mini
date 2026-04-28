"""Schema checks for benchmark tasks and model outputs."""

from __future__ import annotations

from typing import Any


TASK_REQUIRED = {
    "task_id",
    "track",
    "species",
    "genome_id",
    "genome_name",
    "assembly_path",
    "visible_evidence",
    "gold",
    "provenance",
}

OUTPUT_REQUIRED = {"task_id", "answer", "confidence", "evidence", "rationale", "uncertainty"}

MECHREASON_LAYERS = ("genome", "protein", "mechanism", "cell", "phenotype")

VALID_TRACKS = {"genopheno", "dbreconcile", "mechreason"}
VALID_PHENOTYPES = {"Resistant", "Susceptible", "Intermediate", "Non-susceptible", "Insufficient evidence"}
VALID_MECHANISM_CLASSES = {
    "enzymatic_inactivation",
    "target_modification",
    "target_protection",
    "efflux",
    "permeability_loss",
    "regulator_loss_of_function",
    "metabolic_bypass",
    "intrinsic",
    "insufficient_evidence",
}

# Optional fields capture cases where two mechanisms genuinely co-drive resistance
# (e.g., ESBL hyperexpression + porin loss → carbapenem R). They are off by default;
# auditors fill them in for ambiguous hybrid cases. The primary mechanism remains
# the dominant call, so existing scoring is unaffected when these fields are empty.
VALID_INTERACTION_TYPES = {"additive", "synergistic", "uncertain"}
VALID_DISAGREEMENT_TYPES = {
    "same_call_different_name",
    "gene_family_vs_allele",
    "threshold_difference",
    "database_version_difference",
    "drug_mapping_difference",
    "intrinsic_vs_acquired",
    "species_scope_difference",
    "point_mutation_vs_gene_presence",
    "partial_or_low_quality_hit",
    "true_conflict",
    "insufficient_evidence",
}


def validate_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(TASK_REQUIRED - set(task))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    track = task.get("track")
    if track not in VALID_TRACKS:
        errors.append(f"invalid track: {track!r}")

    if not isinstance(task.get("visible_evidence"), dict):
        errors.append("visible_evidence must be an object")
    if not isinstance(task.get("gold"), dict):
        errors.append("gold must be an object")
    if not isinstance(task.get("provenance"), dict):
        errors.append("provenance must be an object")

    if track == "genopheno":
        if "antibiotic" not in task:
            errors.append("genopheno task missing antibiotic")
        phenotype = task.get("gold", {}).get("phenotype")
        if phenotype not in VALID_PHENOTYPES:
            errors.append(f"invalid gold phenotype: {phenotype!r}")

    if track == "dbreconcile":
        dtype = task.get("gold", {}).get("disagreement_type")
        if dtype not in VALID_DISAGREEMENT_TYPES:
            errors.append(f"invalid disagreement_type: {dtype!r}")
        if "target" not in task:
            errors.append("dbreconcile task missing target")

    if track == "mechreason":
        if "antibiotic" not in task:
            errors.append("mechreason task missing antibiotic")
        gold = task.get("gold", {})
        mech_class = gold.get("mechanism_class")
        if mech_class not in VALID_MECHANISM_CLASSES:
            errors.append(f"invalid mechanism_class: {mech_class!r}")
        if not isinstance(gold.get("required_genes"), list):
            errors.append("mechreason gold missing required_genes list")
        if gold.get("phenotype") not in VALID_PHENOTYPES:
            errors.append(f"mechreason gold has invalid phenotype: {gold.get('phenotype')!r}")
        secondary = gold.get("secondary_mechanism_classes")
        if secondary is not None:
            if not isinstance(secondary, list):
                errors.append("mechreason gold secondary_mechanism_classes must be a list when present")
            else:
                bad = [c for c in secondary if c not in VALID_MECHANISM_CLASSES]
                if bad:
                    errors.append(f"invalid secondary_mechanism_classes: {bad!r}")
        interaction = gold.get("interaction_type")
        if interaction is not None and interaction not in VALID_INTERACTION_TYPES:
            errors.append(f"invalid interaction_type: {interaction!r}")

    return errors


def validate_output(output: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(OUTPUT_REQUIRED - set(output))
    if missing:
        errors.append(f"missing required output fields: {', '.join(missing)}")

    confidence = output.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append("confidence must be a number in [0, 1]")

    if not isinstance(output.get("evidence"), list):
        errors.append("evidence must be a list")

    return errors
