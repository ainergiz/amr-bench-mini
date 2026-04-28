"""CARD ARO substrate lookup.

Parses ``data/card/aro_index.tsv`` and exposes a small lookup function that
maps a gene name (as it appears in AMRFinderPlus or ResFinder hits) to its
CARD ARO entries: AMR Gene Family, Drug Class coverage, and Resistance
Mechanism. Used to construct a deterministic substrate-context block that can
be optionally injected into the agent's prompt.

The matcher is intentionally lenient: it normalizes gene names by stripping
``bla`` prefixes, parentheses, primes, hyphens, and casing, then compares the
normalized forms. A gene matches a CARD entry when either the entry's
``CARD Short Name`` or ``ARO Name`` normalizes to a string that contains the
normalized query (or vice versa).
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARO_INDEX = ROOT / "data" / "card" / "aro_index.tsv"


@dataclass(frozen=True)
class CardEntry:
    aro: str
    card_short_name: str
    aro_name: str
    family: str
    drug_classes: tuple[str, ...]
    mechanism: str


_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def _normalize(name: str) -> str:
    s = (name or "").lower().strip()
    if s.startswith("bla"):
        s = s[3:]
    return _NON_ALNUM.sub("", s)


def _split_drug_classes(raw: str) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(s.strip() for s in raw.split(";") if s.strip())


@lru_cache(maxsize=1)
def load_card_entries() -> list[CardEntry]:
    if not ARO_INDEX.exists():
        return []
    out: list[CardEntry] = []
    with ARO_INDEX.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            out.append(
                CardEntry(
                    aro=row.get("ARO Accession", "").strip(),
                    card_short_name=row.get("CARD Short Name", "").strip(),
                    aro_name=row.get("ARO Name", "").strip(),
                    family=row.get("AMR Gene Family", "").strip(),
                    drug_classes=_split_drug_classes(row.get("Drug Class", "")),
                    mechanism=row.get("Resistance Mechanism", "").strip(),
                )
            )
    return out


@lru_cache(maxsize=1)
def _norm_index() -> list[tuple[str, str, CardEntry]]:
    """Return [(normalized_short_name, normalized_aro_name, entry), ...]."""
    return [
        (_normalize(e.card_short_name), _normalize(e.aro_name), e)
        for e in load_card_entries()
    ]


_MIN_TOKEN = 4  # Minimum normalized-name length for substring matching.


def lookup(gene: str, *, max_matches: int = 4) -> list[CardEntry]:
    """Return up to ``max_matches`` CARD entries matching ``gene``.

    Matching priority:
        1. Exact normalized-name match (CARD Short Name or ARO Name).
        2. Query is a strict prefix of a normalized name (catches gene-allele
           queries like ``blaSHV-28`` resolving to the SHV-28 entry).
        3. Both query and candidate normalize to length >= MIN_TOKEN and one
           is a substring of the other (catches near-allelic variants like
           ``aac(6')-Ib-cr5`` resolving to ``AAC(6')-Ib-cr``).
    Short normalized strings (e.g., ``Bla1`` → ``1``) are excluded from the
    substring rule to avoid spurious matches.
    """
    if not gene:
        return []
    q = _normalize(gene)
    if not q:
        return []
    exact: list[CardEntry] = []
    prefix: list[CardEntry] = []
    substring: list[CardEntry] = []
    for nshort, nname, entry in _norm_index():
        if q == nshort or q == nname:
            exact.append(entry)
            continue
        if (nshort and nshort.startswith(q) and len(q) >= _MIN_TOKEN) or (
            nname and nname.startswith(q) and len(q) >= _MIN_TOKEN
        ):
            prefix.append(entry)
            continue
        if len(q) >= _MIN_TOKEN:
            for cand in (nshort, nname):
                if not cand or len(cand) < _MIN_TOKEN:
                    continue
                if q in cand or cand in q:
                    substring.append(entry)
                    break
    seen: set[str] = set()
    out: list[CardEntry] = []
    for entry in exact + prefix + substring:
        if entry.aro in seen:
            continue
        seen.add(entry.aro)
        out.append(entry)
        if len(out) >= max_matches:
            break
    return out


def lookup_for_genes(genes: list[str], *, max_matches: int = 4) -> dict[str, list[CardEntry]]:
    return {g: lookup(g, max_matches=max_matches) for g in genes}


def render_context_block(genes: list[str], *, max_matches_per_gene: int = 3) -> str:
    """Format CARD substrate annotations for inclusion in a prompt.

    Returns an empty string when no genes resolve to any CARD entry. Otherwise
    returns a markdown-style block listing each gene's matched CARD families,
    drug-class coverage, and resistance mechanism.
    """
    rows: list[str] = []
    seen_genes: set[str] = set()
    for gene in genes:
        if not gene or gene in seen_genes:
            continue
        seen_genes.add(gene)
        matches = lookup(gene, max_matches=max_matches_per_gene)
        if not matches:
            rows.append(f"- `{gene}`: no CARD ARO entry matched")
            continue
        for entry in matches:
            drugs = "; ".join(entry.drug_classes) if entry.drug_classes else "—"
            rows.append(
                f"- `{gene}` → {entry.aro} ({entry.card_short_name or entry.aro_name}); "
                f"family: {entry.family or '—'}; drug-class coverage: {drugs}; "
                f"mechanism: {entry.mechanism or '—'}"
            )
    if not rows:
        return ""
    header = (
        "CARD ARO substrate annotations (from data/card/aro_index.tsv). "
        "These are mechanism+substrate-class mappings, not isolate-specific evidence; "
        "use them to judge whether a visible gene's substrate spectrum covers the "
        "queried antibiotic."
    )
    return header + "\n" + "\n".join(rows)
