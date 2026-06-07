# Paper camera-ready draft — AMR-Bench-mini

**Target:** FM4LS @ ICML 2026 (workshop poster paper)
**OpenReview status:** ICML 2026 FM4LS Workshop Poster, published 2026-05-28
**Camera-ready style:** ICML 2026 template, using
`\usepackage[accepted]{icml2026}` with the accepted notice adjusted for the
FM4LS workshop.

## Files

- `paper.tex` — full camera-ready workshop paper built with the ICML 2026
  style.
- `icml2026.sty`, `icml2026.bst`, `fancyhdr.sty`, `algorithm.sty`,
  `algorithmic.sty` — ICML 2026 style files, with the accepted notice updated
  for the FM4LS camera-ready.
- `refs.bib` — verified bibliography entries derived from the project
  literature-review notes, with DOI and venue details checked for submission.
- Tables 1--2 — headline split and hard-category results generated from the
  checked-in result artifacts.

## Building

The style files are checked into this directory for local builds. The accepted
notice in `icml2026.sty` is workshop-specific and names FM4LS rather than the
main ICML/PMLR proceedings.

```bash
cd paper && latexmk -pdf -interaction=nonstopmode paper.tex
```

Current official-template build: 5 PDF pages total.

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
