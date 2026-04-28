# AMR-MechBench — paper idea, locked

**Target:** GenBio @ ICML 2026 — *Generative and Agentic AI for Biology* · deadline **2026-05-01 AOE** (6 days from now).

**Format:** short (4 pp) or long (9 pp), non-archival, dual submission OK · OpenReview · ICML LaTeX template via [Overleaf](https://www.overleaf.com/read/dnjfbdnypxwn#79923f).

---

## Status snapshot — Day 1, 2026-04-25 19:30

**3-track benchmark scaffold is live and tested.** 24/24 unit tests pass.

> **Important nuance about the corpus state:** 60 K. pneumoniae isolates with WGS + lab AST have been *pulled* into `data/` (1,536 AST records, 60 FASTAs, 60 metadata records). The current task set in `data/tasks/*.jsonl` is built from the **10-isolate subset that has both AMRFinderPlus *and* ResFinder complete** — that subset yields 212 GenoPheno + 150 DBReconcile + 162 MechReason = 524 tasks. AMRFinderPlus is currently at 60/60; ResFinder is at 34/60 (~5 min remaining); once ResFinder finishes we will rebuild tasks against the full corpus and expect ~5–6× growth in MechReason tasks plus more `insufficient_evidence` HypothesisGen seeds.

| Artifact | Count / status |
|---|---|
| K. pneumoniae isolates pulled (WGS + lab AST) | **60** |
| Lab-evidence AST records | **1,536** |
| AMRFinderPlus annotator outputs | **60/60 ✅** |
| ResFinder annotator outputs | **34/60** (running) |
| Isolates with both annotators complete | **10** (defines the current task corpus) |
| GenoPheno tasks (current 10-isolate corpus) | 212 |
| DBReconcile tasks (current 10-isolate corpus) | 150 |
| **MechReason tasks (current 10-isolate corpus)** | **162** across 8 mechanism classes |
| Total benchmark tasks (current corpus) | **524** |
| Rule baseline accuracy on current corpus | 89.7% overall · 100% MechReason — *infrastructure check only, not a real baseline number; the heuristic echoes the gold* |
| Tests | 24/24 passing |

**MechReason mechanism-class distribution (162 tasks):**
- `enzymatic_inactivation`: 64 (β-lactamases + AMEs)
- `permeability_loss`: 57 (ompK35/36 frameshifts)
- `target_modification`: 14 (gyrA/parC QRDR + colistin lipid-A)
- `metabolic_bypass`: 11 (dfrA + sul)
- `efflux`: 7
- `regulator_loss_of_function`: 5 (ramR/acrR LoF)
- `insufficient_evidence`: 3 *(seeds for HypothesisGen sub-track — agent must recognize the gap)*
- `intrinsic`: 1 (chromosomal fosA)

**Code is structured as a proper Python package** (`src/amr_bench/`) with schema validation, scoring with rubric subscores, deterministic rule baseline, and a provider-agnostic LLM agent harness ready for Anthropic / OpenAI inference (parser tested without network calls).

**What's been pivoted vs. the original spike (clinical AMR-Bench):**
- ❌ Dropped EmpiricRx track — pure clinical CDSS, wrong venue.
- ⚠️ GenoPheno kept as a gateway track ("can the agent get the simple version right?").
- ⚠️ DBReconcile kept (gene-vs-gene reasoning is biology, not clinical care).
- ✅ **Added MechReason as the headline track** with 5-layer schema (genome → protein → mechanism → cell → phenotype) and a fixed mechanism-class vocabulary.
- ✅ README explicit safety-scope: *retrospective evidence synthesis, not patient treatment, not pathogen engineering, not antibiotic design.*

**What's blocked next:**
- API key from user for Day 2 (Anthropic and/or OpenAI). Spike-tier budget ~$10–30/agent on Sonnet 4.6.
- Author + colleague involvement for Day 3 HypothesisGen case curation.

---

## One-sentence pitch

> A benchmark and tool-augmented scaffold for **agentic AI doing multi-scale biological reasoning** on antimicrobial resistance — connecting **nucleotide → protein → mechanism → cellular pathway → phenotype** — evaluated on real *K. pneumoniae* isolates, including held-out cases where annotator output alone cannot explain the phenotype.

---

## What's wrong with the field

1. **No public benchmark evaluates multi-scale mechanistic AMR reasoning by agents.** Existing general bio/science benchmarks (LAB-Bench, BixBench, Biomni-Eval1, ScienceAgentBench, ChemBench) contain isolated AMR or antibiotic-related examples, but none evaluate genome → protein → mechanism → cellular pathway → phenotype chains. (Confirmed across the lit review.)
2. **Existing AMR work is single-scale.** AMRscope predicts variant pathogenicity at the protein level; LLMTB predicts MTB resistance from genomes; clinical CDSS papers predict S/I/R. **None of them reason across scales** the way a microbiologist does — "this gyrA double mutant is resistant *because* the protein's QRDR loses fluoroquinolone binding *because* serine 83 hydrogen-bonds the drug *because* this organism's intact porins still admit the drug to the periplasm where the mutated GyrA is."
3. **Annotator-driven phenotype prediction has well-known failure modes** that are not measured anywhere. The spike (see `amr-bench/outputs/agent_trial_step3.md`) surfaced six recurring high-value subtleties — and no published benchmark surfaces these:
   1. OXA-48 + intact porins → meropenem usually S despite a "carbapenemase" annotation
   2. aac(6')-Ib-cr variants → variable amikacin MIC
   3. Chromosomal regulator LoF (ramR / acrR / oqxR / marR) drives tigecycline + chloramphenicol R but neither AMRFinder nor ResFinder annotates these point mutations
   4. Chromosomal *fosA* in *K. pneumoniae* gives elevated fosfomycin MIC but is often phenotypically S
   5. Intermediate (I) phenotypes are systematically collapsed to S/R by phenotype predictors
   6. Tigecycline R driven by efflux-regulator overexpression — visible annotators may flag adjacent genes (oqxA, oqxB, tet(A)) but those alone do not explain phenotype

These three together = white space we can occupy in 6 days.

---

## What we propose

### Two tracks

**Track 1 — MechReason** *(reuses 100% of spike data)*
Given an isolate's WGS + a drug + the laboratory AST phenotype, the agent must produce a **5-layer mechanistic explanation**:

| Layer | What the agent must produce |
|---|---|
| **L1 — Genome** | Specific gene/variant, location (chromosome vs plasmid), mobile-genetic-element context |
| **L2 — Protein** | Protein identity, native function, structural class, how variant affects structure |
| **L3 — Mechanism** | Catalytic / binding / efflux mechanism; substrate specificity where relevant |
| **L4 — Cell** | Cellular compartment, pathway interactions, regulatory upstream |
| **L5 — Phenotype** | Semi-quantitative mechanistic chain from molecular event to observed MIC (no numerical MIC modeling) |

Each layer is rubric-scored. Total: 7 dimensions per case (gene-correct, protein-correct, mechanism-class-correct, structural-plausibility, cell-pathway-correct, multi-scale-coherence, hidden-mechanism-acknowledged).

**Track 2 — HypothesisGen** *(the headline contribution)*
For the subset of cases where annotator output is **insufficient** to explain the phenotype (e.g., AST shows tigecycline R; AMRFinder + ResFinder flag tigecycline-adjacent genes such as `oqxA`, `oqxB`, `tet(A)`, but those alone do not fully explain the phenotype because the dominant mechanism is chromosomal regulator LoF that neither tool annotates), the agent must:
1. Recognize the gap.
2. Propose a biological hypothesis explaining the discrepancy.
3. Specify the validation step (e.g., "BLAST `ramR` ORF against reference; expect frameshift").

Eval: held-out post-cutoff literature where the answer was published (Imperial × Google AI co-scientist did this at small scale; we systematize it).

### Tool stack the agent has access to

The contribution isn't just "we built another benchmark" — it's "**we showed which tool augmentations improve multi-scale biological reasoning, and quantified the failure modes that remain.**" Tools:

1. **AMRFinderPlus** (NCBI, validated by spike, 73 s/isolate)
2. **ResFinder** (validated by spike, 12 s/isolate)
3. **CARD/RGI** (Day-1: pip-install with latest CARD JSON; Docker image was stale)
4. **MOB-suite + PlasmidFinder** — plasmid vs chromosomal localization
5. **AlphaFold / ESM-Fold lookup** — structural reasoning (active-site geometry, pocket clashes)
6. **BLAST + reference-ORF alignment** — regulator frameshift / premature stop detection (the *modal* unannotated mechanism)
7. **PaperQA / PubMed search** — citation grounding for mechanism claims
8. **CARD ARO ontology** — mechanism class taxonomy

**Required vs optional tool calls** is one of the three open decisions below.

---

## Why this fits GenBio (CFP topic mapping)

| CFP topic | How we hit it |
|---|---|
| Topic 2: Agent-based hypothesis generation | HypothesisGen track is the primary contribution |
| Topic 3: FMs for multi-scale biology | The 5-layer schema is the operational definition of multi-scale reasoning across molecules → cells → organisms |
| Topic 4: Benchmarks for autonomous scientific systems | The dataset + rubric + tool stack |
| Topic 6: Safety, governance, ethical considerations | Biosecurity guardrails section: no novel-resistance-engineering tasks, no zoonotic enhancement |

We do **not** claim to fit topic 1 (generative biomolecule design — SAGA owns this) or topic 5 (human-AI collab in research labs — we don't have a real lab).

---

## Differentiation against existing work

| System / paper | What they did | Why we're different |
|---|---|---|
| **SAGA** (Du, Jin et al., 2025) | Bi-level objective evolution → wet-lab-validated novel antibiotic | We do *mechanism understanding*, not *de novo design*. Complementary, not competitive. |
| **Fleming** (Wei et al., 2025) | Multi-agent system for Mtb antibiotic design | Same — design vs. mechanism reasoning. |
| **Google AI Co-scientist** (2025) | Generate-debate-evolve, demonstrated AMR mechanism rediscovery at Imperial | Closed-source, anecdotal demo. We systematize it as a public benchmark. |
| **Biomni** (Stanford, 2025) | Generalist biomedical agent, 150 tools, 25 subfields | No AMR track. We're a domain-vertical specialization with deeper biology. |
| **AMRscope** (Sanger, 2025) | ESM-2 + MLP for AMR variant prediction | Single-protein, single-scale; not agentic; no clinical/mechanistic chain. We use AMRscope as a tool inside our agent. |
| **LAB-Bench / BixBench** | Biology MCQ + bioinformatics in Jupyter | No AMR coverage; no multi-scale schema. We're complementary domain coverage. |
| **CRISPR-GPT** | Closed agent for gene editing | Same architectural template; we apply it to mechanism reasoning, not editing design. |

---

## Author moat

- **ID/AMR domain expertise** (user + colleague): designing the 5-layer rubric, identifying genuinely puzzling HypothesisGen cases, calibrating the LLM-judge on mechanism quality. This is irreplaceable — no other team can do this in 6 days.
- **Production agent engineering**: implementing the tool stack and ReAct loop is straightforward for the author.
- **Spike infrastructure already built**: BV-BRC pipeline, two annotators, parsers, agent harness, three test cases run.

---

## Spike + Day-1 evidence (already collected)

**Spike artifacts (2026-04-25, ~90 min):**
- `amr-bench/data/`: started at 322 lab-evidence AST records on 10 isolates → **now 1,536 AST records on 60 isolates**.
- `amr-bench/outputs/amrfinder/`, `outputs/resfinder/`: AMR annotator outputs (10 done, 50 running for new isolates).
- `amr-bench/outputs/agent_trial_step3.md`: GenoPheno me-as-agent reasoning hit 85.1% with a 4-mode failure taxonomy that becomes the headline.
- `amr-bench/outputs/agent_trial_step4.md`: EmpiricRx case sanity check (since *deprecated* — clinical, not biology).
- `amr-bench/outputs/mechreason_trial.md`: 3 multi-scale reasoning cases (KPC+VIM, OXA-48 + intact porins, tigecycline regulator) run end-to-end with self-rubric. Case B is the **discrimination point** (gene says R, biology-aware reasoning says S). Case C is the **HypothesisGen exemplar** (annotators silent; mechanism class = `insufficient_evidence`; agent must propose hypothesis).
- `spike-results.md`: GO memo.

**Day-1 artifacts (2026-04-25 PM):**
- `src/amr_bench/agent.py`: provider-agnostic LLM agent harness with Anthropic + OpenAI adapters; tested JSON-response parser tolerates fenced and unfenced output.
- `src/amr_bench/schema.py`: extended with `mechreason` track and `VALID_MECHANISM_CLASSES` (9-class vocabulary).
- `src/amr_bench/scoring.py`: 4-component MechReason scoring — `mechanism_class_correct` ∧ `gene_family_correct` ∧ `layers_complete` (binary) + `tools_called` flag (for Day-2 stratification).
- `scripts/build_tasks.py`: priority-ordered `infer_mechanism()` covering 9 mechanism classes; produces 162 MechReason tasks deterministically.
- `scripts/scale_isolates.py`: idempotent BV-BRC pull; took the corpus from 10 → 60 isolates in ~5 min.
- `scripts/run_annotators.sh`: parallel Docker runner for AMRFinderPlus + ResFinder; running in background as of 19:00.
- `tests/test_mechreason.py`, `tests/test_agent.py`: 14 new unit tests covering inference, scoring, schema validation, and prompt rendering.

**Spike findings that informed Day-1 design choices:**

1. **BV-BRC API > FTP.** The FTP endpoint is unreliable from this network; the `genome_sequence` API works at 5–10 MB/isolate. Already automated in `pull_fasta.py`.
2. **64% of BV-BRC AST is "Computational Method", not laboratory.** All pulls now filter `evidence == "Laboratory Method"` to keep ground truth honest.
3. **AMRFinderPlus + ResFinder cover ~95% of expected disagreement signal** for K. pneumoniae. RGI/CARD adds value but its current Docker image is stale (CARD JSON schema mismatch); pip install is blocked by uv-managed Python. **Decision:** v1 ships with two annotators; RGI is Day-2 venv work or post-deadline.
4. **Real disagreements are mostly allele-precision, not gene-presence.** Spike showed 8–17 disagreements per isolate dominated by SHV-allele ambiguity (AMRFinder=SHV-11; ResFinder lists 7 candidates including ESBL SHV-13 — clinical impact is real because SHV-11 is broad-spectrum, SHV-13 is ESBL).
5. **Multi-scale reasoning is the right discriminator.** Me-as-agent at 85% on naive GenoPheno; failures cluster around exactly the cases biology-aware reasoning should solve (OXA-48 weak hydrolyzer + intact porins; chromosomal regulator LoF; aac(6')-Ib-cr variable amikacin MIC; chromosomal fosA overcalling). These become the headline failure-mode taxonomy.
6. **Rule baseline at 100% on MechReason is expected, not concerning.** The rule echoes the gold heuristic — it sets a *floor* and confirms scoring infrastructure is wired. Real signal comes from (a) LLM-judge layer-quality scoring on L1–L5 narrative depth, (b) tool-stratified accuracy on `insufficient_evidence` HypothesisGen cases, where the rule baseline trivially fails to *recognize* the gap.

---

## Concrete deliverables (target by 2026-05-01)

1. **Dataset** — 100–200 *K. pneumoniae* + ideally cross-pathogen slice (A. baumannii / E. coli / S. aureus). · ✅ **60 K. pneumoniae done; cross-pathogen pull is Day-2 stretch.**
2. **Eval harness** — Python harness scoring rubric dimensions per case via LLM-judge. · ✅ **Schema + 3 binary subscores + tool-stratification flag implemented; LLM-judge layer-quality scorer is Day 2.**
3. **Tool-augmented agent scaffold** — provider-agnostic ReAct loop + 8 tools. · ⚠️ **Harness scaffold + JSON parser tested; only AMRFinder/ResFinder lookups currently implemented; remaining 4 tool wrappers are Day 2.**
4. **Baselines** — rule baseline + vanilla ReAct (Sonnet 4.6) + Biomni + our scaffold. · ⚠️ **Rule baseline runs at 89.7% overall (100% MechReason — *infrastructure check only*, not a real baseline number; the rule echoes the gold heuristic so this is label echo); LLM baselines are Day 4.**
5. **Failure-mode taxonomy** — 4–6 categories with reproducible triggers. · ⚠️ **6 documented from spike (OXA-48 + intact porins; aac(6')-Ib-cr; chromosomal regulators; fosA chromosomal; intermediate phenotypes; tigecycline regulators); needs trace-driven empirical validation Day 4–5.**
6. **HypothesisGen subset** — 20–40 puzzling cases. · ⚠️ **3 auto-detected as `insufficient_evidence` so far on 10-isolate corpus; expect ~20–40 once 50 new annotator runs land.**
7. **Paper** — 4 pp short or 9 pp long. · ⏳ Day 5 onward.

---

## Locked decisions (committed Day 1)

1. **Schema depth: 5 layers** (`genome / protein / mechanism / cell / phenotype`) in agent output; **scoring collapsed to 3 binary checks** (`mechanism_class_correct`, `gene_family_correct`, `layers_complete`) plus an LLM-judge Likert for layer-quality on Day 2. Implemented in `src/amr_bench/scoring.py`.
2. **HypothesisGen ground truth: hybrid.** v1 uses author + colleague + LLM-judge calibrated rubric. Post-cutoff literature curation flagged as v2 work for the camera-ready / future paper.
3. **Tool calls: optional but rewarded.** The agent has access to all tools, doesn't fail if it skips, but final eval reports **tool-stratified accuracy** ("agent + AMRFinder/ResFinder only" vs "agent + structural + literature retrieval"). This is the cleanest way to demonstrate the value of the tool stack as a methods contribution.

These are committed in code (schema.py, scoring.py, agent.py). Trivial to revisit before submission if the LLM-judge calibration says otherwise.

---

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| 6-day timeline too tight for 9-pp long paper | Trim ladder: drop HypothesisGen → MechReason-only short paper. Drop multi-pathogen → K. pneumoniae only. |
| LLM-judge inconsistency on 5-layer rubric | Author-calibrate on 20 cases; use Sonnet 4.6 as judge with chain-of-thought |
| RGI/CARD installation pain (Docker stale) | pip install + load latest CARD JSON; alternative: drop RGI, use AMRFinder + ResFinder + custom CARD ARO lookup |
| BV-BRC AST has duplicates per isolate-drug | Dedup logic in `build_tasks.py` (use most recent + most stringent method) |
| HypothesisGen hard to ground without published answers | Lean on expert (author + colleague) rubric for v1; flag as Day-1 limitation |
| Reviewers say "this is clinical microbiology" | The 5-layer schema + structural/cellular/multi-scale framing + HypothesisGen track puts the paper firmly in biological reasoning, not clinical decision support. EmpiricRx is dropped. |

---

## High-level Day 1–6 plan

- **Apr 25 (Fri) — Day 1: ~70% done.**
  - ✅ Scaled isolates 10 → 60 K. pneumoniae (1,536 lab AST records).
  - ✅ Refactored task spec: added 162 MechReason tasks with 5-layer schema + 9-class mechanism vocabulary.
  - ✅ Wrote agent harness scaffold + provider adapters + JSON parser.
  - ✅ 24/24 unit tests passing.
  - ⏳ AMRFinderPlus + ResFinder annotation on 50 new isolates running in background (~14 min wall).
  - ❌ RGI install blocked (uv-managed Python); deferred to Day-2 venv or post-deadline.
- **Apr 26 (Sat) — Day 2:** add remaining tool wrappers (CARD ARO lookup, BLAST regulator-ORF, AlphaFold/UniProt structure summary, PaperQA / PubMed retrieval); rebuild tasks with full 60-isolate corpus (~1k MechReason tasks expected); first-pass MechReason eval with vanilla Sonnet 4.6 ReAct; LLM-judge for layer-quality.
- **Apr 27 (Sun) — Day 3:** curate 20–40 HypothesisGen cases (author + colleague); calibrate LLM-judge on 20 author-graded cases; refine rubric.
- **Apr 28 (Mon) — Day 4:** run all 3 baselines (vanilla, Biomni, our scaffold) on full benchmark; collect traces.
- **Apr 29 (Tue) — Day 5:** failure-mode taxonomy from traces; figures; main eval table; writing (Intro / Related Work / Method / Experiments).
- **Apr 30 (Wed) — Day 6 buffer:** Discussion / Limitations / Biosecurity sections.
- **May 1 (Thu) — submit by AOE.**

API budget estimate: $50–200 (Sonnet 4.6 primary; Haiku 4.5 + GPT-5-mini cross-checks; Opus 4.7 only on a 100-task headline subsample). Open-weight baseline (optional, GPU): Llama-3.1-70B / Qwen3 for cost-quality curve.

---

## Pointers

- Lit review (4 streams synthesized): `/Users/ainergiz/iclr/genbio-litreview.md`
- Spike memo (Day-0 GO/NO-GO): `/Users/ainergiz/iclr/spike-results.md`
- This doc (canonical idea + Day-1 status): `/Users/ainergiz/iclr/amr-mechbench-idea.md`
- Workshop info & deadlines: `/Users/ainergiz/iclr/icml-2026-workshops.md`

**Codebase pointers:**
- Project root: `/Users/ainergiz/iclr/amr-bench/`
- Package: `src/amr_bench/{schema,parsing,prompts,scoring,baselines,agent,io}.py`
- Scripts: `scripts/{pull_isolates,pull_fasta,scale_isolates,build_tasks,run_baselines,run_annotators,make_manual_audit}.{py,sh}`
- Tests: `tests/{test_parsing,test_schema,test_scoring,test_mechreason,test_agent}.py`
- Generated tasks: `data/tasks/{genopheno,dbreconcile,mechreason}.jsonl`
- Generated artifacts: `outputs/{task_bundles,dataset_summary}.json`, `results/rule_baseline_summary.{json,md}`
- Trial reasoning: `outputs/{agent_trial_step3,agent_trial_step4,mechreason_trial}.md`
