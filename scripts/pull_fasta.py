#!/usr/bin/env python3
"""Pull FASTA via BV-BRC genome_sequence API (FTP doesn't work for assemblies)."""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FASTA = DATA / "fasta"
FASTA.mkdir(exist_ok=True)

ISOLATES = [
    "573.18477", "573.24267", "573.18476", "573.24386", "573.15595",
    "573.24380", "573.24407", "573.24245", "573.24349", "573.15602",
]

API = "https://www.bv-brc.org/api/genome_sequence"

for gid in ISOLATES:
    out = FASTA / f"{gid}.fna"
    if out.exists() and out.stat().st_size > 0:
        print(f"  {gid} already present ({out.stat().st_size} bytes)")
        continue
    url = (
        f"{API}/?eq(genome_id,{gid})"
        f"&select(sequence_id,sequence_type,length,sequence)"
        f"&limit(500)&http_accept=application/json"
    )
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read().decode())
    lines = []
    total = 0
    for s in data:
        seq = s.get("sequence", "")
        sid = s.get("sequence_id", "")
        stype = s.get("sequence_type", "")
        lines.append(f">{sid} type={stype} length={len(seq)}")
        for i in range(0, len(seq), 70):
            lines.append(seq[i : i + 70])
        total += len(seq)
    out.write_text("\n".join(lines) + "\n")
    print(f"  {gid}: {len(data)} contigs, {total:,} bp -> {out.name}")

print("\nDone.")
