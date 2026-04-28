#!/usr/bin/env python3
"""Pull 10 K. pneumoniae isolates from BV-BRC with rich AST panels + FASTA."""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

BVBRC = "https://www.bv-brc.org/api"

# Top 10 isolates by panel size (from Step 1 query)
ISOLATES = [
    "573.18477", "573.24267", "573.18476", "573.24386", "573.15595",
    "573.24380", "573.24407", "573.24245", "573.24349", "573.15602",
]


def fetch_json(path: str, query: str) -> list:
    url = f"{BVBRC}/{path}/?{query}&http_accept=application/json"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode()


def main():
    ast_records = []
    for gid in ISOLATES:
        q = (
            f"and(eq(genome_id,{gid}),eq(evidence,Laboratory+Method))"
            "&select(genome_id,genome_name,antibiotic,resistant_phenotype,"
            "measurement,measurement_unit,measurement_sign,laboratory_typing_method,"
            "testing_standard,testing_standard_year)&limit(50)"
        )
        rows = fetch_json("genome_amr", q)
        ast_records.extend(rows)
        print(f"  {gid}: {len(rows)} AST records")

    out = DATA / "ast.json"
    out.write_text(json.dumps(ast_records, indent=2))
    print(f"Wrote {len(ast_records)} AST records to {out}")

    # Fetch genome metadata
    metas = []
    for gid in ISOLATES:
        q = f"eq(genome_id,{gid})&select(genome_id,genome_name,strain,mlst,host_name,isolation_country,collection_year,sequencing_status,genome_length,contigs,gc_content)&limit(1)"
        r = fetch_json("genome", q)
        if r:
            metas.append(r[0])
    (DATA / "metadata.json").write_text(json.dumps(metas, indent=2))
    print(f"Wrote {len(metas)} metadata records")

    # Fetch FASTAs
    fasta_dir = DATA / "fasta"
    fasta_dir.mkdir(exist_ok=True)
    for gid in ISOLATES:
        out_path = fasta_dir / f"{gid}.fna"
        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"  {gid} FASTA already present ({out_path.stat().st_size} bytes)")
            continue
        # FTP path: ftp://ftp.bvbrc.org/genomes/<gid>/<gid>.fna
        url = f"https://ftp.bvbrc.org/genomes/{gid}/{gid}.fna"
        try:
            text = fetch_text(url)
            out_path.write_text(text)
            print(f"  {gid} FASTA: {len(text)} bytes")
        except Exception as e:
            print(f"  {gid} FASTA FAILED: {e}")
        time.sleep(0.3)

    print("\nDone.")


if __name__ == "__main__":
    main()
