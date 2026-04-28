#!/usr/bin/env python3
"""Scale BV-BRC isolate set: target 50–60 K. pneumoniae with rich AST panels.

Filters BV-BRC for taxon_id=573, evidence=Laboratory Method, and selects isolates
ranked by AST drug-panel size. Skips isolates already pulled. Writes appended
ast.json + metadata.json + per-isolate FASTA.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FASTA = DATA / "fasta"
FASTA.mkdir(exist_ok=True)

TARGET_TOTAL = 60
BVBRC = "https://www.bv-brc.org/api"

EXISTING_IDS = {"573.18477", "573.24267", "573.18476", "573.24386", "573.15595",
                "573.24380", "573.24407", "573.24245", "573.24349", "573.15602"}


def fetch_json(path: str, query: str) -> list:
    url = f"{BVBRC}/{path}/?{query}&http_accept=application/json"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def main() -> None:
    print("Fetching panel-size ranking from BV-BRC ...")
    rows = fetch_json(
        "genome_amr",
        "and(eq(taxon_id,573),eq(evidence,Laboratory+Method))&select(genome_id)&limit(50000)",
    )
    counts = Counter(r["genome_id"] for r in rows)
    candidates = [gid for gid, _c in counts.most_common(400) if gid not in EXISTING_IDS]
    needed = TARGET_TOTAL - len(EXISTING_IDS)
    candidates = candidates[: needed * 2]  # buffer for any failures
    print(f"  candidate pool: {len(candidates)} new isolates (need {needed})")

    pulled: list[str] = []
    new_ast: list[dict] = []
    new_meta: list[dict] = []

    for gid in candidates:
        if len(pulled) >= needed:
            break
        # Pull AST
        ast = fetch_json(
            "genome_amr",
            f"and(eq(genome_id,{gid}),eq(evidence,Laboratory+Method))"
            "&select(genome_id,genome_name,antibiotic,resistant_phenotype,"
            "measurement,measurement_unit,measurement_sign,laboratory_typing_method,"
            "testing_standard,testing_standard_year)&limit(50)",
        )
        if len(ast) < 8:
            continue
        # Pull genome metadata
        meta = fetch_json(
            "genome",
            f"eq(genome_id,{gid})&select(genome_id,genome_name,strain,mlst,host_name,isolation_country,collection_year,sequencing_status,genome_length,contigs,gc_content)&limit(1)",
        )
        if not meta:
            continue
        # Pull FASTA via genome_sequence API
        out_path = FASTA / f"{gid}.fna"
        if not out_path.exists() or out_path.stat().st_size == 0:
            seqs = fetch_json(
                "genome_sequence",
                f"eq(genome_id,{gid})&select(sequence_id,sequence_type,length,sequence)&limit(500)",
            )
            if not seqs:
                continue
            lines: list[str] = []
            total = 0
            for s in seqs:
                seq = s.get("sequence", "")
                lines.append(f">{s.get('sequence_id','')} type={s.get('sequence_type','')} length={len(seq)}")
                for i in range(0, len(seq), 70):
                    lines.append(seq[i : i + 70])
                total += len(seq)
            out_path.write_text("\n".join(lines) + "\n")

        new_ast.extend(ast)
        new_meta.extend(meta)
        pulled.append(gid)
        print(f"  + {gid}: {len(ast)} AST records, contigs in FASTA")
        time.sleep(0.25)

    # Merge with existing ast.json + metadata.json
    ast_path = DATA / "ast.json"
    meta_path = DATA / "metadata.json"
    existing_ast = json.loads(ast_path.read_text()) if ast_path.exists() else []
    existing_meta = json.loads(meta_path.read_text()) if meta_path.exists() else []
    merged_ast = existing_ast + new_ast
    existing_meta_ids = {m["genome_id"] for m in existing_meta}
    merged_meta = existing_meta + [m for m in new_meta if m["genome_id"] not in existing_meta_ids]
    ast_path.write_text(json.dumps(merged_ast, indent=2))
    meta_path.write_text(json.dumps(merged_meta, indent=2))
    print(f"\nNew isolates pulled: {len(pulled)}")
    print(f"AST records total: {len(merged_ast)}")
    print(f"Genomes total: {len(merged_meta)}")
    print(f"FASTA files: {len(list(FASTA.glob('*.fna')))}")


if __name__ == "__main__":
    main()
