# Paper draft — AMR-Bench-mini

**Target:** GenBio @ ICML 2026 (4-page short paper)
**Deadline:** 2026-05-01 AOE

## Files

- `paper.tex` — full short-paper draft built directly with the GenBio-linked
  ICML 2026 style.
- `icml2026.sty`, `icml2026.bst`, `fancyhdr.sty`, `algorithm.sty`,
  `algorithmic.sty` — copied from the official GenBio Overleaf template
  linked in the CFP.
- `refs.bib` — verified bibliography entries derived from
  `genbio-litreview.md`, with DOI and venue details checked for submission.
- Figure 1 — inline TikZ UpSet-style failure-overlap diagram in `paper.tex`.

## Building

The GenBio CFP links the read-only Overleaf template at
<https://www.overleaf.com/read/dnjfbdnypxwn>. The official style files are now
checked into this directory for local builds. Rechecked against a fresh
download from that Overleaf project on 2026-04-26; `icml2026.sty`,
`icml2026.bst`, `fancyhdr.sty`, `algorithm.sty`, and `algorithmic.sty`
matched byte-for-byte.

```bash
cd paper && latexmk -pdf -interaction=nonstopmode paper.tex
```

Current official-template build: 5 PDF pages total, with technical body on
pages 1--4 and references beginning on page 4. GenBio excludes references and
appendices from the 4-page short-paper limit.

## Numbers in the paper, with their source

| Claim | Source artifact |
|---|---|
| Pilot strict / adjusted accuracies | `results/headline_table.json` |
| Hard-split strict / adjusted accuracies | `results/headline_table.json` |
| Wilson 95% CIs | computed in `scripts/build_headline_table.py` |
| Per-category hard-split accuracy | `results/headline_table.md` (per-category section) |
| Audit-loop counts (31, 22 KEEP, etc.) | `results/mechreason_audit/audit_summary.md` |
| Tool null effect (32/50 = 32/50) | `results/tool_vs_baseline_gemini_hard.md` |
| 924 corpus task count | `outputs/dataset_summary.json` |
| Annotator versions | `outputs/provenance.json` |

## Remaining optional checks

- [ ] Optionally rerun the full 924-task corpus on Gemini batch + Claude batch
  for a one-paragraph scale-validation footnote in §3 or §4.
- [ ] Final page-count sanity check after any further text or reference edits.
