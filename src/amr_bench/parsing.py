"""Parsers and normalization helpers for AMR-Bench-mini artifacts."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from amr_bench.io import read_json


ANTIBIOTIC_CLASSES: dict[str, str] = {
    "amikacin": "aminoglycoside",
    "amoxicillin": "beta-lactam",
    "amoxicillin/clavulanic acid": "beta-lactam",
    "ampicillin": "beta-lactam",
    "aztreonam": "beta-lactam",
    "cefazolin": "beta-lactam",
    "cefepime": "beta-lactam",
    "cefotaxime": "beta-lactam",
    "cefotaxime/clavulanic acid": "beta-lactam",
    "cefotetan": "beta-lactam",
    "cefoxitin": "beta-lactam",
    "ceftaroline": "beta-lactam",
    "ceftazidime": "beta-lactam",
    "ceftazidime/clavulanic acid": "beta-lactam",
    "ceftriaxone": "beta-lactam",
    "cefuroxime": "beta-lactam",
    "cephalothin": "beta-lactam",
    "ciprofloxacin": "quinolone",
    "colistin": "polymyxin",
    "doripenem": "beta-lactam",
    "ertapenem": "beta-lactam",
    "fosfomycin": "fosfomycin",
    "gentamicin": "aminoglycoside",
    "imipenem": "beta-lactam",
    "levofloxacin": "quinolone",
    "meropenem": "beta-lactam",
    "moxifloxacin": "quinolone",
    "nitrofurantoin": "nitrofuran",
    "norfloxacin": "quinolone",
    "piperacillin": "beta-lactam",
    "piperacillin/tazobactam": "beta-lactam",
    "polymyxin b": "polymyxin",
    "sulfamethoxazole": "folate pathway antagonist",
    "tetracycline": "tetracycline",
    "ticarcillin/clavulanic acid": "beta-lactam",
    "tigecycline": "tetracycline",
    "tobramycin": "aminoglycoside",
    "trimethoprim": "folate pathway antagonist",
    "trimethoprim/sulfamethoxazole": "folate pathway antagonist",
}

ANTIBIOTIC_ALIASES: dict[str, tuple[str, ...]] = {
    "amoxicillin/clavulanic acid": ("amoxicillin+clavulanic acid", "amoxicillin clavulanic acid"),
    "piperacillin/tazobactam": ("piperacillin+tazobactam", "piperacillin tazobactam"),
    "ticarcillin/clavulanic acid": ("ticarcillin+clavulanic acid", "ticarcillin clavulanic acid"),
    "trimethoprim/sulfamethoxazole": ("trimethoprim", "sulfamethoxazole", "trimethoprim sulfamethoxazole"),
    "polymyxin b": ("polymyxin b", "polymyxin"),
    "rifampin": ("rifampicin",),
}


def norm_text(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("_", " ")
    value = value.replace("-", " ")
    value = re.sub(r"\s+", " ", value)
    return value


def norm_drug(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("+", "/")
    value = re.sub(r"\s+", " ", value)
    return value


def norm_gene(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def gene_family(value: str) -> str:
    """Return a coarse family key for common AMR gene naming patterns."""
    raw = value.strip()
    lower = raw.lower()
    compact = norm_gene(lower)

    if compact.startswith("blashv"):
        return "blashv"
    if compact.startswith("blatem"):
        return "blatem"
    if compact.startswith("blakpc"):
        return "blakpc"
    if compact.startswith("blavim"):
        return "blavim"
    if compact.startswith("blaoxa"):
        return "blaoxa"
    if compact.startswith("fos"):
        return re.sub(r"\d+$", "", compact)
    if compact.startswith("dfra"):
        return "dfra"
    if compact.startswith("aada"):
        return "aada"
    if compact.startswith("oqxa"):
        return "oqxa"
    if compact.startswith("oqxb"):
        return "oqxb"
    if compact.startswith("aac"):
        return re.sub(r"\d+$", "", compact)
    if compact.startswith("aph"):
        return re.sub(r"\d+$", "", compact)

    mutation_match = re.match(r"([a-z]{3,4})[_-]?[a-z]\d+[a-z]$", lower)
    if mutation_match:
        return mutation_match.group(1)

    return re.sub(r"\d+$", "", compact)


def is_point_mutation_call(row: dict[str, Any]) -> bool:
    method = str(row.get("method", "")).upper()
    gene = str(row.get("gene", ""))
    return method.startswith("POINT") or bool(re.search(r"_[A-Z]\d+[A-Z]$", gene))


def parse_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_metadata(path: Path) -> dict[str, dict[str, Any]]:
    return {row["genome_id"]: row for row in read_json(path)}


def load_ast_records(path: Path) -> list[dict[str, Any]]:
    return read_json(path)


def group_ast(records: list[dict[str, Any]]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        gid = row.get("genome_id")
        drug = norm_drug(str(row.get("antibiotic", "")))
        phenotype = row.get("resistant_phenotype")
        if not gid or not drug or not phenotype:
            continue
        grouped[gid][drug].append(row)
    return grouped


def collapse_ast_record(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not records:
        return None
    phenotypes = {str(row.get("resistant_phenotype", "")).strip() for row in records if row.get("resistant_phenotype")}
    if len(phenotypes) != 1:
        return None
    first = records[0]
    return {
        "phenotype": first.get("resistant_phenotype", ""),
        "measurement": first.get("measurement", ""),
        "measurement_unit": first.get("measurement_unit", ""),
        "measurement_sign": first.get("measurement_sign", ""),
        "laboratory_typing_method": first.get("laboratory_typing_method", ""),
        "testing_standard": first.get("testing_standard", ""),
        "testing_standard_year": first.get("testing_standard_year", ""),
        "source_records": records,
    }


def parse_amrfinder(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if row.get("Type") != "AMR":
                continue
            rows.append(
                {
                    "source": "AMRFinderPlus",
                    "gene": row.get("Element symbol", ""),
                    "element_name": row.get("Element name", ""),
                    "scope": row.get("Scope", ""),
                    "type": row.get("Type", ""),
                    "drug_class": row.get("Class", ""),
                    "subclass": row.get("Subclass", ""),
                    "method": row.get("Method", ""),
                    "identity": parse_float(row.get("% Identity to reference")),
                    "coverage": parse_float(row.get("% Coverage of reference")),
                    "ref_acc": row.get("Closest reference accession", ""),
                    "ref_name": row.get("Closest reference name", ""),
                }
            )
    return dedupe_hits(rows)


def parse_resfinder(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open() as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            gene = row.get("Resistance gene", "")
            if not gene:
                continue
            rows.append(
                {
                    "source": "ResFinder",
                    "gene": gene,
                    "phenotype": row.get("Phenotype", ""),
                    "identity": parse_float(row.get("Identity")),
                    "coverage": parse_float(row.get("Coverage")),
                    "ref_acc": row.get("Accession no.", ""),
                    "position": row.get("Position in contig", ""),
                    "contig": row.get("Contig", ""),
                }
            )
    return dedupe_hits(rows)


def dedupe_hits(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str, str]] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        key = (
            str(row.get("source", "")),
            str(row.get("gene", "")).lower(),
            str(row.get("ref_acc", "")),
            str(row.get("method", "")),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def antibiotic_terms(drug: str) -> set[str]:
    drug = norm_drug(drug)
    terms = {drug, norm_text(drug)}
    for alias in ANTIBIOTIC_ALIASES.get(drug, ()):
        terms.add(norm_drug(alias))
        terms.add(norm_text(alias))
    class_name = ANTIBIOTIC_CLASSES.get(drug)
    if class_name:
        terms.add(norm_text(class_name))
    return terms


def hit_matches_antibiotic(hit: dict[str, Any], drug: str) -> bool:
    drug = norm_drug(drug)
    terms = antibiotic_terms(drug)
    source = hit.get("source")

    if source == "ResFinder":
        phenotype = norm_text(str(hit.get("phenotype", "")))
        if any(term in phenotype for term in terms):
            return True
        if ANTIBIOTIC_CLASSES.get(drug) == "beta-lactam" and "beta lactam" in phenotype:
            return True
        return False

    if source == "AMRFinderPlus":
        haystack = norm_text(f"{hit.get('drug_class', '')} {hit.get('subclass', '')} {hit.get('element_name', '')}")
        if any(term in haystack for term in terms):
            return True
        class_name = ANTIBIOTIC_CLASSES.get(drug, "")
        if class_name == "beta-lactam" and "beta lactam" in haystack:
            return True
        if class_name == "quinolone" and "quinolone" in haystack:
            return True
        if class_name == "folate pathway antagonist" and (
            "trimethoprim" in haystack or "sulfonamide" in haystack or "diaminopyrimidine" in haystack
        ):
            return True
        if drug == "colistin" and "polymyxin" in haystack:
            return True
        return False

    return False


def relevant_hits(hits: list[dict[str, Any]], drug: str, limit: int = 12) -> list[dict[str, Any]]:
    matched = [hit for hit in hits if hit_matches_antibiotic(hit, drug)]
    return sorted(matched, key=lambda row: (row.get("source", ""), row.get("gene", "")))[:limit]


def source_versions(resfinder_json: Path | None = None) -> dict[str, str]:
    versions = {
        "BV-BRC": "local pull; see data/metadata.json and data/ast.json",
        "AMRFinderPlus": "precomputed local TSV; executable/version not detected in current shell",
        "ResFinder": "precomputed local output",
    }
    if resfinder_json and resfinder_json.exists():
        try:
            data = read_json(resfinder_json)
            version = data.get("software_version")
            run_date = data.get("run_date")
            if version:
                versions["ResFinder"] = f"{version}" + (f" ({run_date})" if run_date else "")
        except Exception:
            pass
    return versions
