#!/usr/bin/env python3
"""Build AMR-Bench-mini task JSONL from local AST and annotation artifacts."""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import write_json, write_jsonl  # noqa: E402
from amr_bench.parsing import (  # noqa: E402
    ANTIBIOTIC_CLASSES,
    collapse_ast_record,
    gene_family,
    group_ast,
    is_point_mutation_call,
    load_ast_records,
    load_metadata,
    norm_drug,
    norm_gene,
    parse_amrfinder,
    parse_resfinder,
    relevant_hits,
    source_versions,
)
from amr_bench.schema import validate_task  # noqa: E402

DATA = ROOT / "data"
OUT = ROOT / "outputs"
TASKS = DATA / "tasks"


def main() -> None:
    metadata = load_metadata(DATA / "metadata.json")
    ast_records = load_ast_records(DATA / "ast.json")
    ast = group_ast(ast_records)
    source_version_map = source_versions(next((OUT / "resfinder").glob("*/573.json"), None))

    bundles = build_bundles(metadata, ast)
    write_json(OUT / "task_bundles.json", bundles)

    genopheno = build_genopheno_tasks(bundles, source_version_map)
    dbreconcile = build_dbreconcile_tasks(bundles, source_version_map)
    mechreason = build_mechreason_tasks(bundles, source_version_map)

    validate_tasks(genopheno + dbreconcile + mechreason)
    write_jsonl(TASKS / "genopheno.jsonl", genopheno)
    write_jsonl(TASKS / "dbreconcile.jsonl", dbreconcile)
    write_jsonl(TASKS / "mechreason.jsonl", mechreason)

    summary = summarize(bundles, genopheno, dbreconcile, mechreason)
    write_json(OUT / "dataset_summary.json", summary)

    print(f"Wrote {len(genopheno)} GenoPheno tasks -> {TASKS / 'genopheno.jsonl'}")
    print(f"Wrote {len(dbreconcile)} DBReconcile tasks -> {TASKS / 'dbreconcile.jsonl'}")
    print(f"Wrote {len(mechreason)} MechReason tasks -> {TASKS / 'mechreason.jsonl'}")
    print(f"Wrote dataset summary -> {OUT / 'dataset_summary.json'}")


def build_bundles(metadata: dict[str, dict[str, Any]], ast: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
    bundles: list[dict[str, Any]] = []
    for gid in sorted(metadata):
        amrfinder_hits = parse_amrfinder(OUT / "amrfinder" / f"{gid}.tsv")
        resfinder_hits = parse_resfinder(OUT / "resfinder" / gid / "ResFinder_results_tab.txt")
        bundle = {
            "genome_id": gid,
            "metadata": metadata[gid],
            "assembly_path": f"data/fasta/{gid}.fna",
            "amrfinder_hits": amrfinder_hits,
            "resfinder_hits": resfinder_hits,
            "ast": ast.get(gid, {}),
        }
        bundles.append(bundle)
        print(
            f"{gid}: AMRFinder={len(amrfinder_hits)} hits "
            f"ResFinder={len(resfinder_hits)} hits AST={len(ast.get(gid, {}))} drugs"
        )
    return bundles


def build_genopheno_tasks(bundles: list[dict[str, Any]], versions: dict[str, str]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    index = 1
    for bundle in bundles:
        metadata = bundle["metadata"]
        all_hits = bundle["amrfinder_hits"] + bundle["resfinder_hits"]
        for drug, records in sorted(bundle["ast"].items()):
            drug = norm_drug(drug)
            if drug not in ANTIBIOTIC_CLASSES:
                continue
            collapsed = collapse_ast_record(records)
            if collapsed is None:
                continue
            hits = relevant_hits(all_hits, drug)
            task = {
                "task_id": f"genopheno_kp_{index:06d}",
                "track": "genopheno",
                "species": "Klebsiella pneumoniae",
                "genome_id": bundle["genome_id"],
                "genome_name": metadata.get("genome_name", ""),
                "assembly_path": bundle["assembly_path"],
                "antibiotic": drug,
                "antibiotic_class": ANTIBIOTIC_CLASSES[drug],
                "metadata": public_metadata(metadata),
                "visible_evidence": {
                    "labels_visible": False,
                    "relevant_tool_hits": hits,
                    "tool_hit_count": len(hits),
                    "all_amrfinder_hit_count": len(bundle["amrfinder_hits"]),
                    "all_resfinder_hit_count": len(bundle["resfinder_hits"]),
                },
                "gold": collapsed,
                "provenance": {
                    "data_source": "BV-BRC genome, metadata, and laboratory AST records",
                    "tool_versions": versions,
                    "notes": "Retrospective benchmark label; not a clinical recommendation.",
                },
            }
            tasks.append(task)
            index += 1
    return tasks


def build_dbreconcile_tasks(bundles: list[dict[str, Any]], versions: dict[str, str]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    index = 1
    for bundle in bundles:
        metadata = bundle["metadata"]
        family_map: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: {"amrfinder": [], "resfinder": []})
        for hit in bundle["amrfinder_hits"]:
            family_map[gene_family(hit.get("gene", ""))]["amrfinder"].append(hit)
        for hit in bundle["resfinder_hits"]:
            family_map[gene_family(hit.get("gene", ""))]["resfinder"].append(hit)

        for family in sorted(family_map):
            if not family:
                continue
            amr = family_map[family]["amrfinder"]
            res = family_map[family]["resfinder"]
            dtype = classify_disagreement(amr, res)
            if dtype is None:
                continue
            task = {
                "task_id": f"dbreconcile_kp_{index:06d}",
                "track": "dbreconcile",
                "species": "Klebsiella pneumoniae",
                "genome_id": bundle["genome_id"],
                "genome_name": metadata.get("genome_name", ""),
                "assembly_path": bundle["assembly_path"],
                "target": {
                    "gene_family": family,
                    "amrfinder_gene_names": sorted({hit.get("gene", "") for hit in amr}),
                    "resfinder_gene_names": sorted({hit.get("gene", "") for hit in res}),
                },
                "metadata": public_metadata(metadata),
                "visible_evidence": {
                    "amrfinder_hits": amr[:8],
                    "resfinder_hits": res[:8],
                    "labels_visible": False,
                },
                "gold": {
                    "disagreement_type": dtype,
                    "expected_resolution": expected_resolution(dtype),
                },
                "provenance": {
                    "data_source": "Precomputed AMRFinderPlus and ResFinder outputs on the same local assembly",
                    "tool_versions": versions,
                    "notes": "Gold disagreement labels are heuristic pilot labels and should be manually audited before publication.",
                },
            }
            tasks.append(task)
            index += 1
    return tasks


def build_mechreason_tasks(bundles: list[dict[str, Any]], versions: dict[str, str]) -> list[dict[str, Any]]:
    """One MechReason task per (isolate, drug) pair where AST phenotype + visible evidence support a deterministic gold mechanism class.

    Cases that intentionally land on `insufficient_evidence` are kept as gold so that
    the agent must recognize the gap and propose a hypothesis (the HypothesisGen
    flavor of MechReason). This is the discrimination point.
    """
    tasks: list[dict[str, Any]] = []
    index = 1
    for bundle in bundles:
        metadata = bundle["metadata"]
        all_hits = bundle["amrfinder_hits"] + bundle["resfinder_hits"]
        for drug, records in sorted(bundle["ast"].items()):
            drug = norm_drug(drug)
            if drug not in ANTIBIOTIC_CLASSES:
                continue
            collapsed = collapse_ast_record(records)
            if collapsed is None:
                continue
            phenotype = collapsed["phenotype"]
            if phenotype not in {"Resistant", "Intermediate", "Non-susceptible"}:
                continue  # MechReason only asks "why R" — S phenotypes have no resistance mechanism to explain
            hits = relevant_hits(all_hits, drug)
            mechanism_class, required_genes, rationale = infer_mechanism(drug, hits)
            task = {
                "task_id": f"mechreason_kp_{index:06d}",
                "track": "mechreason",
                "species": "Klebsiella pneumoniae",
                "genome_id": bundle["genome_id"],
                "genome_name": metadata.get("genome_name", ""),
                "assembly_path": bundle["assembly_path"],
                "antibiotic": drug,
                "antibiotic_class": ANTIBIOTIC_CLASSES[drug],
                "metadata": public_metadata(metadata),
                "visible_evidence": {
                    "labels_visible": False,
                    "phenotype_visible": True,
                    "ast_phenotype": phenotype,
                    "relevant_tool_hits": hits,
                    "tool_hit_count": len(hits),
                    "all_amrfinder_hit_count": len(bundle["amrfinder_hits"]),
                    "all_resfinder_hit_count": len(bundle["resfinder_hits"]),
                },
                "gold": {
                    "phenotype": phenotype,
                    "mechanism_class": mechanism_class,
                    "required_genes": required_genes,
                    "rationale": rationale,
                },
                "provenance": {
                    "data_source": "BV-BRC genome and laboratory AST + AMRFinderPlus and ResFinder annotations",
                    "tool_versions": versions,
                    "notes": "Gold mechanism is a heuristic from gene-class priors and should be audited; cases of insufficient_evidence are intentionally retained to surface the HypothesisGen sub-track.",
                },
            }
            tasks.append(task)
            index += 1
    return tasks


def infer_mechanism(drug: str, hits: list[dict[str, Any]]) -> tuple[str, list[str], str]:
    """Map (drug, relevant tool hits) -> (mechanism_class, required_genes, rationale).

    Priority-ordered. Returns ``insufficient_evidence`` when no rule fires; this
    signals a HypothesisGen-flavored case where the annotators alone cannot
    explain a Resistant/Intermediate phenotype.
    """
    drug = norm_drug(drug)
    drug_class = ANTIBIOTIC_CLASSES.get(drug, "")
    gene_names = [str(hit.get("gene", "")) for hit in hits]
    compact = [norm_gene(name) for name in gene_names]

    point_genes = [name for hit, name in zip(hits, compact) if is_point_mutation_call(hit)]
    bla_genes = [g for g in compact if g.startswith("bla")]

    def bla_family_starts_with(gene_compact: str, prefixes: tuple[str, ...]) -> bool:
        """Match against a β-lactamase family by stripping the ``bla`` prefix
        before checking. Avoids false positives like ``act`` matching inside
        ``blactxm15`` (= blaCTX-M-15)."""
        name = gene_compact[3:] if gene_compact.startswith("bla") else gene_compact
        return any(name.startswith(p) for p in prefixes)

    has_carbapenemase = any(
        bla_family_starts_with(g, ("kpc", "vim", "ndm", "imp", "oxa48", "oxa181", "oxa232", "oxa162", "oxa204"))
        for g in bla_genes
    )
    # AmpC β-lactamases hydrolyze cefoxitin; ESBLs and narrow-spectrum SHV/TEM/OXA do not.
    has_ampc = any(
        bla_family_starts_with(g, ("cmy", "dha", "fox", "mox", "acc", "act", "mir"))
        for g in bla_genes
    )
    has_porin_loss = any("ompk35" in g or "ompk36" in g for g in point_genes)
    regulator_loss_genes = [g for g in point_genes if any(reg in g for reg in ("ramr", "acrr", "marr", "oqxr", "soxr"))]
    direct_tet_efflux = [g for g in compact if g.startswith("teta") or g.startswith("tetb") or g.startswith("tetc") or g.startswith("tetd") or g.startswith("tete") or g.startswith("tetg") or g.startswith("teth") or g.startswith("tetk") or g.startswith("tetl") or g.startswith("tetx") or g.startswith("tety")]

    # Carbapenem-specific permeability loss: only meaningful when no carbapenemase.
    # For non-carbapenem β-lactams, porin loss is rarely the dominant mechanism
    # because direct β-lactamase hydrolysis is typically sufficient.
    is_carbapenem_drug = drug in {"ertapenem", "imipenem", "meropenem", "doripenem"}
    if is_carbapenem_drug and not has_carbapenemase and has_porin_loss:
        return (
            "permeability_loss",
            sorted({g for g in point_genes if "ompk" in g}),
            "Porin loss in OmpK35/OmpK36 reduces periplasmic carbapenem accumulation; no carbapenemase detected so this is the dominant mechanism.",
        )

    # Cefoxitin biology fix: cefoxitin (a 7α-methoxy cephamycin) is hydrolyzed by:
    #   * AmpC β-lactamases (CMY/DHA/FOX/MOX/ACC/ACT/MIR);
    #   * KPC-family class-A serine carbapenemases (KPC-2/3 have good cefoxitin activity);
    #   * some metallo-β-lactamases (NDM, VIM at moderate level).
    # Cefoxitin is NOT efficiently hydrolyzed by ESBLs (CTX-M family), narrow SHV/TEM,
    # or class-D OXA enzymes (OXA-1, OXA-9). So the priority is:
    #   * If AmpC or carbapenemase (KPC/NDM/VIM) present       -> enzymatic_inactivation
    #   * If only non-cefoxitin-hydrolyzing β-lactamases + ompK loss -> permeability_loss
    #   * Otherwise                                            -> insufficient_evidence
    cefoxitin_active_genes = [
        g for g in bla_genes
        if bla_family_starts_with(g, ("cmy", "dha", "fox", "mox", "acc", "act", "mir", "kpc", "ndm", "vim"))
    ]
    if drug == "cefoxitin":
        if cefoxitin_active_genes:
            return (
                "enzymatic_inactivation",
                sorted(set(cefoxitin_active_genes)),
                "AmpC β-lactamase or KPC/NDM/VIM-family carbapenemase hydrolyzes the 7α-methoxy cephamycin cefoxitin.",
            )
        if has_porin_loss:
            return (
                "permeability_loss",
                sorted({g for g in point_genes if "ompk" in g}),
                "Cefoxitin R driven by porin loss; non-AmpC β-lactamases (CTX-M, narrow SHV/TEM, OXA-1) cannot hydrolyze cefoxitin and are confounders here.",
            )
        # Fall through to insufficient_evidence — non-cefoxitin-hydrolyzing β-lactamases alone do not explain cefoxitin R.

    # Regulator LoF takes priority for tigecycline (its modal mechanism in K. pneumoniae).
    if drug == "tigecycline" and regulator_loss_genes:
        return (
            "regulator_loss_of_function",
            sorted(set(regulator_loss_genes)),
            "Loss-of-function in efflux regulator(s) derepresses AcrAB-TolC and related pumps; modal tigecycline-R mechanism in K. pneumoniae.",
        )

    # Tigecycline biology fix: wild-type tet(A) and oqxAB do not give tigecycline R
    # (tigecycline is a glycylcycline designed to evade Tet pumps). Without a
    # regulator LoF or a known tigecycline-active tet variant (tet(X), tet(L)),
    # the visible evidence is insufficient to explain a clinical R phenotype.
    if drug == "tigecycline":
        tigecycline_capable = [g for g in direct_tet_efflux if "tetx" in g or "tetl" in g]
        if not tigecycline_capable and not regulator_loss_genes:
            return (
                "insufficient_evidence",
                [],
                "Wild-type tet(A) and oqxAB cannot drive tigecycline R; no regulator LoF (ramR/acrR/oqxR/marR) nor tigecycline-active tet variant detected. HypothesisGen flavor.",
            )

    # Target modification — point mutations in primary target
    if drug_class == "quinolone":
        target_genes = [g for g in point_genes if any(t in g for t in ("gyra", "gyrb", "parc", "pare"))]
        if target_genes:
            return (
                "target_modification",
                sorted(set(target_genes)),
                "QRDR mutation in gyrase or topoisomerase IV target reduces fluoroquinolone binding.",
            )
    if drug == "colistin":
        target_genes = [g for g in point_genes if any(t in g for t in ("mgrb", "pmrb", "pmra", "phop", "phoq"))]
        target_genes += [g for g in compact if g.startswith("mcr")]
        if target_genes:
            return (
                "target_modification",
                sorted(set(target_genes)),
                "Lipid A modification (PEtN addition or lipid biosynthesis change) reduces polymyxin binding.",
            )

    # Tetracycline (specifically) priority fix: when a direct tet-efflux pump is
    # present, that pump is the dominant mechanism; ramR/acrR LoF is supplementary.
    # This avoids the heuristic-priority bug where tet(A)+ramR for tetracycline
    # was being labeled regulator_loss_of_function even though tet(A) alone is
    # sufficient for tetracycline R.
    if drug == "tetracycline" and direct_tet_efflux:
        return (
            "efflux",
            sorted(set(direct_tet_efflux)),
            "Direct tetracycline-specific MFS efflux pump (tet) confers tetracycline R; any regulator LoF is supplementary.",
        )

    # Enzymatic inactivation — beta-lactamases, AMEs.
    if drug_class == "beta-lactam":
        if bla_genes:
            return (
                "enzymatic_inactivation",
                sorted(set(bla_genes)),
                "β-lactamase hydrolyzes the β-lactam ring; phenotype depends on enzyme class and porin status.",
            )

    # If we still see ompK frameshifts at this point and no β-lactamase fired,
    # treat them as a non-carbapenem permeability_loss case (rare).
    if drug_class == "beta-lactam" and has_porin_loss:
        return (
            "permeability_loss",
            sorted({g for g in point_genes if "ompk" in g}),
            "Porin loss in OmpK35/OmpK36 with no β-lactamase visible; permeability is the only annotated mechanism.",
        )

    # Generic regulator LoF as fallback for tetracycline-class drugs without a
    # direct drug-specific efflux pump (handled above) — chloramphenicol /
    # macrolide / phenicol cases mostly.
    if regulator_loss_genes and drug_class in {"phenicol", "macrolide"}:
        return (
            "regulator_loss_of_function",
            sorted(set(regulator_loss_genes)),
            "Loss-of-function in efflux regulator(s) derepresses multidrug efflux pumps.",
        )
    # Tetracycline + regulator LoF without direct tet efflux falls here too.
    if regulator_loss_genes and drug == "tetracycline" and not direct_tet_efflux:
        return (
            "regulator_loss_of_function",
            sorted(set(regulator_loss_genes)),
            "Loss-of-function in efflux regulator(s) derepresses AcrAB-TolC; no direct tet-specific efflux pump present.",
        )

    if drug_class == "aminoglycoside":
        ame_genes = [g for g in compact if g.startswith("aac") or g.startswith("aph") or g.startswith("aad") or g.startswith("ant") or g.startswith("aacae")]
        if ame_genes:
            return (
                "enzymatic_inactivation",
                sorted(set(ame_genes)),
                "Aminoglycoside-modifying enzyme (AME) acetylates, phosphorylates, or adenylates the drug.",
            )

    if drug == "fosfomycin":
        fos_genes = [g for g in compact if g.startswith("fos")]
        if fos_genes:
            return (
                "intrinsic",
                sorted(set(fos_genes)),
                "Klebsiella encodes a chromosomal fosA-family glutathione transferase; intrinsic elevation of fosfomycin MIC.",
            )

    # Metabolic bypass — folate pathway antagonists
    if drug_class == "folate pathway antagonist":
        bypass_genes = [g for g in compact if g.startswith("dfra") or g.startswith("sul")]
        if bypass_genes:
            return (
                "metabolic_bypass",
                sorted(set(bypass_genes)),
                "Acquired drug-insensitive DHFR (dfr) and/or DHPS (sul) bypass the inhibited folate-pathway enzyme.",
            )

    # Efflux fallback (excluding the tet/tigecycline cases handled above).
    if drug_class in {"tetracycline", "phenicol", "macrolide", "nitrofuran", "fluoroquinolone"}:
        efflux_genes = [g for g in compact if g.startswith("tet") or g.startswith("oqx") or g.startswith("acr") or g.startswith("mef") or g.startswith("mphr") or g.startswith("mph") or g.startswith("mdf")]
        if efflux_genes:
            return (
                "efflux",
                sorted(set(efflux_genes)),
                "Active efflux pumps reduce intracellular drug accumulation.",
            )

    # No rule fired — annotator evidence does not explain the phenotype
    return (
        "insufficient_evidence",
        [],
        "Visible annotator evidence does not deterministically map to a mechanism for this drug; HypothesisGen flavor.",
    )


def classify_disagreement(amr: list[dict[str, Any]], res: list[dict[str, Any]]) -> str | None:
    if not amr and not res:
        return None
    if amr and not res and any(is_point_mutation_call(row) for row in amr):
        return "point_mutation_vs_gene_presence"
    if not amr and res:
        return "threshold_difference"
    if amr and not res:
        return "threshold_difference"
    amr_names = {norm_gene(row.get("gene", "")) for row in amr}
    res_names = {norm_gene(row.get("gene", "")) for row in res}
    if amr_names & res_names:
        return "drug_mapping_difference"
    return "gene_family_vs_allele"


def expected_resolution(dtype: str) -> str:
    if dtype == "point_mutation_vs_gene_presence":
        return "Do not force an acquired-gene comparison; report that one source captures a mutation-style call outside the other source's acquired-gene scope."
    if dtype == "drug_mapping_difference":
        return "Treat the calls as compatible at gene level while noting that drug/class mappings are exposed at different granularity."
    if dtype == "gene_family_vs_allele":
        return "Treat the calls as potentially compatible at family level but not identical at allele/name level."
    if dtype == "threshold_difference":
        return "Report a source-specific hit and avoid deciding which database is correct without version and threshold review."
    return "Report insufficient evidence."


def public_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    fields = [
        "strain",
        "mlst",
        "collection_year",
        "isolation_country",
        "sequencing_status",
        "genome_length",
        "contigs",
        "gc_content",
        "host_name",
    ]
    return {field: metadata.get(field) for field in fields if field in metadata}


def validate_tasks(tasks: list[dict[str, Any]]) -> None:
    failures: list[str] = []
    for task in tasks:
        errors = validate_task(task)
        if errors:
            failures.append(f"{task.get('task_id', '<missing>')}: {'; '.join(errors)}")
    if failures:
        raise SystemExit("Task validation failed:\n" + "\n".join(failures[:20]))


def summarize(
    bundles: list[dict[str, Any]],
    genopheno: list[dict[str, Any]],
    dbreconcile: list[dict[str, Any]],
    mechreason: list[dict[str, Any]],
) -> dict[str, Any]:
    antibiotic_counts = Counter(task["antibiotic"] for task in genopheno)
    phenotype_counts = Counter(task["gold"]["phenotype"] for task in genopheno)
    disagreement_counts = Counter(task["gold"]["disagreement_type"] for task in dbreconcile)
    mechanism_counts = Counter(task["gold"]["mechanism_class"] for task in mechreason)
    mech_drug_counts = Counter(task["antibiotic"] for task in mechreason)
    return {
        "species": ["Klebsiella pneumoniae"],
        "isolate_count": len(bundles),
        "genopheno_task_count": len(genopheno),
        "dbreconcile_task_count": len(dbreconcile),
        "mechreason_task_count": len(mechreason),
        "ast_record_count": sum(len(records) for bundle in bundles for records in bundle["ast"].values()),
        "antibiotic_counts": dict(sorted(antibiotic_counts.items())),
        "phenotype_counts": dict(sorted(phenotype_counts.items())),
        "disagreement_type_counts": dict(sorted(disagreement_counts.items())),
        "mechanism_class_counts": dict(sorted(mechanism_counts.items())),
        "mechreason_drug_counts": dict(sorted(mech_drug_counts.items())),
        "amrfinder_hit_counts": {bundle["genome_id"]: len(bundle["amrfinder_hits"]) for bundle in bundles},
        "resfinder_hit_counts": {bundle["genome_id"]: len(bundle["resfinder_hits"]) for bundle in bundles},
    }


if __name__ == "__main__":
    main()
