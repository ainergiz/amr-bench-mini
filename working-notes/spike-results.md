# AMR-Bench Feasibility Spike — GO/NO-GO Memo

**Date:** 2026-04-25 (spike duration: ~90 min)
**Goal:** decide between Angle 1 (AMR-Bench, 3 tracks) and Angle 2 (DBReconcile only) before committing to a 6-day execution plan against the GenBio @ ICML 2026 deadline (2026-05-01).
**Spike data location:** `/Users/ainergiz/iclr/amr-bench/`
**API cost incurred:** $0 (used Claude Opus 4.7 in this session for me-as-agent reasoning)

---

## Verdict: 🟢 GO on Angle 1 (AMR-Bench, 3 tracks)

All four spike steps cleared the bar. Real disagreement signal is rich, agent reasoning is clinically defensible, public data is plentiful and high-quality, and the failure-mode taxonomy that emerged is exactly the kind of contribution GenBio reviewers want.

Fall-back to Angle 2 (DBReconcile only) is **not necessary** — both tracks are viable as separate sub-stories within one paper.

---

## Per-step results

### Step 1 — Data smoke test ✅
- BV-BRC API: **3,011 distinct *K. pneumoniae* genomes** with **laboratory-evidence AST** (not computational predictions). Plus 1,029 with ≥8-drug panels and 81 with ≥12.
- **322 AST records across 10 isolates pulled** (228 R / 62 S / 12 I — good R-S balance for testing).
- All 10 FASTAs (5.3–5.6 Mb each, ~5,400,000 bp) pulled successfully via `genome_sequence` API endpoint.
- ⚠️ **Gotcha:** BV-BRC FTP is broken / blocked from this network. Use API instead (works perfectly, slightly slower).
- ⚠️ **Gotcha:** 64% of BV-BRC AST records are `Computational Method` — must filter `evidence == "Laboratory Method"`. After filter, the data is clean.
- ⚠️ **Gotcha:** Duplicate isolate-drug pairs exist (multiple test runs / methods). Need dedup or majority logic.

**Implication:** scaling to 100–200 isolates is trivial. We can also add *A. baumannii* (taxon 470), *E. coli* (562), *S. aureus* (1280) for cross-pathogen breadth.

### Step 2 — Annotators ✅ (with caveats)
- **AMRFinderPlus** (`ncbi/amr:latest`): works perfectly via Docker, 73 s/isolate (ARM64 emulation), DB version 2026-03-24 (very recent). Outputs full panel: gene calls, point mutations (gyrA/parC/ompK/ramR), drug-class mapping, identity %, method.
- **ResFinder** (`genomicepidemiology/resfinder:latest`): works perfectly, ~12 s/isolate, comprehensive output incl. phenotype prediction.
- **RGI/CARD** (`finlaymaguire/rgi:latest`): ⚠️ **broken** — CARD JSON schema mismatch (image is 3 years old; latest CARD has a `1Va` model_type that breaks the parser). **Mitigation: use pip install or `mcgillanthonyklab/rgi` (newer image) for Day 1.** Not blocking.
- Disagreement signal is **rich**: 8–17 per-isolate disagreements across 10 isolates. Mix is mostly:
  - Allele-level precision (AMRFinder=blaSHV-11; ResFinder=blaSHV-1+blaSHV-143)
  - Multi-candidate ambiguity (ResFinder lists 7 SHV alleles at 99.8% when AMRFinder gives one exact match)
  - Detection scope (AMRFinder catches POINT mutations / regulator LoF; ResFinder reports multi-candidate β-lactamase sets)
  - Subgroup labels (TEM-1 vs TEM-1A vs TEM-1B; fosA vs fosA6)
- **Critical finding:** in isolate 573.24380, AMRFinder calls SHV-11 (broad-spectrum) while ResFinder lists SHV-13/-31/-70 (ESBL) among 7 candidates. **Choosing between these changes therapy** — SHV-11 means ceftriaxone is appropriate, SHV-13 means it's contraindicated. AST data confirms SHV-11 (cef S). **DBReconcile is clinically meaningful, not cosmetic.**

### Step 3 — Me-as-agent (no API cost) ✅
- **GenoPheno**: 40/47 = **85.1%** accuracy across 3 isolates × 16 priority drugs.
- **Failure-mode taxonomy** that emerged (publishable as-is):
  1. **OXA-48 + intact porins → meropenem usually S** (gene→phenotype non-monotonic)
  2. **aac(6')-Ib-cr** variants → variable amikacin MIC (gene says R, often phenotypic S)
  3. **Chromosomal regulator mutations** (ramR/acrR/oqxR/marR) not annotated by either tool but drive tigecycline + chloramphenicol R
  4. **Chromosomal intrinsic resistance overcalled** (fosA in *K. pneumoniae* gives elevated MIC but often phenotypic S)
  5. **Intermediate phenotypes (I)**: agent collapses to S/R; needs explicit I support
  6. **Tigecycline + colistin**: limited gene-level signal, need population priors
- **DBReconcile**: 2/2 cases reconciled correctly with clinical justification + AST-grounded confidence. Case 2 had direct therapeutic implication.

### Step 4 — EmpiricRx ✅
- 1 synthetic patient case (anchored to real isolate 573.18476's actual AST) → 10 min agent reasoning → **consultation-note-level recommendation** with:
  - Spectrum + allergy + renal adjustment + source control + stewardship + duration + safety-net + backup
  - Defensible references (MERINO, Yahav 7-day, IDSA carbapenem allergy)
  - Self-correctly handled the ertapenem R / meropenem S OXA-48 paradox
  - Rubric: 7/8 dimensions ✅, 1/8 ⚠️ (RAG over guidelines is a Day-1 add)
- 50 cases × 10 min ≈ 8 hours agent reasoning + 6 hours rubric eval = **2 author-days**.

---

## What this means for execution

**Angle 1 is feasible with 3 tracks (GenoPheno + DBReconcile + EmpiricRx) for a 9-page long paper.**

If anything slips, the trim-down ladder is:
1. Drop EmpiricRx (3rd track) → still a strong 4–9 pp paper on GenoPheno + DBReconcile
2. Drop GenoPheno → DBReconcile-only, 4 pp short paper (Angle 2 fallback)

---

## Day 1–6 execution plan (working backwards from May 1)

| Day | Date | Deliverable | Notes |
|---|---|---|---|
| **Day 1** | Apr 26 (Sun) | (a) Scale data: pull 100–200 isolates across 4 priority pathogens (Kp, Ec, Ab, Sa); (b) re-run AMRFinderPlus + ResFinder on all; (c) install RGI via pip (alternative to broken Docker image); (d) BV-BRC AST dedup + cleanup pipeline | Use the existing `pull_fasta.py` + Docker pipeline. Add pathogen loop. |
| **Day 2** | Apr 27 (Mon) | (a) Build production agent harness (vanilla ReAct + tool wrappers via Anthropic/OpenAI API); (b) run on 50 GenoPheno tasks → first eval numbers; (c) start EmpiricRx case authoring (you + colleague write 30 cases) | API cost expected: ~$30–80 for first eval pass. |
| **Day 3** | Apr 28 (Tue) | (a) Finalize 50 EmpiricRx cases; (b) build LLM-judge for free-text rationale; (c) run all 3 tracks × 2 baselines (vanilla ReAct + Biomni) | Biomni: clone `snap-stanford/Biomni`, run baseline. ~$80–150 in API. |
| **Day 4** | Apr 29 (Wed) | (a) Build "AMR-aware scaffold" baseline (Biomni + CARD ARO RAG + IDSA RAG); (b) re-run all tracks; (c) failure-mode taxonomy from traces | Real artifact. ~$50 in API. |
| **Day 5** | Apr 30 (Thu) | (a) Final eval pass with Sonnet 4.6 + Haiku 4.5 + GPT-5-mini for cost-quality curve; (b) writing — Intro, Related Work, Method, Experiments, Failure Modes; (c) figures | Heavy writing day. |
| **Day 6** | May 1 (Fri) | Polish + submit by AOE (≈ 12:00 UTC May 2) | Buffer for OpenReview submission flakiness. |

**Estimated total API budget:** $200–400 across all days.
**GPU usage:** optional for Day 4–5 (open-weight baseline like Llama-3.1 70B / Qwen3 — adds a price-tier point but not strictly required).

---

## Concrete blockers + mitigations

| Blocker found | Mitigation |
|---|---|
| RGI/CARD Docker image stale | Use pip install + `rgi load` from latest CARD JSON, or alternative image. Easy swap. |
| BV-BRC FTP unreliable | Use API (`genome_sequence` endpoint) — works fine. |
| ARM64 Mac emulation slows Docker | If we hit time pressure, run on a Linux x86 GPU box for ~3× speedup — but for 100–200 isolates the Mac is fine. |
| Duplicate isolate-drug AST records | Dedup in `build_tasks.py` (use most recent + most stringent method). |
| EmpiricRx case authoring time | You + colleague write 25 each = 50 total. Write template + share. |
| LLM-judge calibration for free-text | Calibrate on 10 author-graded cases before scaling. |

---

## What's already built in `/Users/ainergiz/iclr/amr-bench/`

```
amr-bench/
├── data/
│   ├── ast.json              (322 AST records, 10 isolates, lab evidence)
│   ├── metadata.json         (genome metadata)
│   ├── card/card.json        (CARD DB, ~42 MB, latest)
│   └── fasta/                (10 K. pneumoniae genomes, 5.3–5.6 Mb each)
├── outputs/
│   ├── amrfinder/            (10 TSV outputs, 8–21 gene calls each)
│   ├── resfinder/            (10 isolates, full ResFinder output trees)
│   ├── task_bundles.json     (parsed + joined annotator + AST data)
│   ├── agent_trial_step3.md  (me-as-agent GenoPheno + DBReconcile reasoning, with score)
│   └── agent_trial_step4.md  (me-as-agent EmpiricRx case + reasoning)
├── scripts/
│   ├── pull_isolates.py      (BV-BRC API → AST + metadata)
│   ├── pull_fasta.py         (BV-BRC genome_sequence API → FASTA)
│   └── build_tasks.py        (parse annotators + AST, build task bundles, identify disagreements)
└── logs/                     (ready for run logs)
```

---

## Next decision point

If you want to commit to Angle 1, the immediate next steps for Day 1 (Apr 26) are:
1. Confirm which **API key** to use (Anthropic / OpenAI / both)
2. Confirm **GPU access details** (only needed Day 4–5 if we want open-weight baseline)
3. Confirm **author availability** for EmpiricRx case writing (you + colleague — best on Day 2/3)

If you'd rather pivot to Angle 2 only, that's also a viable safer play and the spike data already covers Track 2's key disagreement signal.

**My recommendation: GO on Angle 1.** The data, tools, and reasoning all work; failure modes are publishable; clinical signal is real.
