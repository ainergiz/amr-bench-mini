# GenBio 2026 AMR Agent Benchmark: Corrected Thesis and Execution Plan

**Working title:** AMR-Bench-mini: A Focused Benchmark for Agentic Antimicrobial Resistance Reasoning  
**Target venue:** GenBio @ ICML 2026  
**Submission deadline:** 2026-05-01 AOE  
**Prepared:** 2026-04-25  
**Local scaffold:** `amr-bench/`  
**Current recommended scope:** two-track benchmark, not the original five-track benchmark  

---

## 1. Executive Decision

The sensible version of the project is a focused benchmark paper:

> Public AMR resources and a few general bio/science benchmarks include isolated AMR or antibiotic-discovery examples, but we found no public AMR-specific, multi-track agent benchmark spanning the practical reasoning tasks that AMR researchers actually face. We introduce a small, reproducible, two-track benchmark for isolate-level AMR reasoning: genotype-to-phenotype evidence synthesis and database/tool-disagreement reconciliation.

This is the right version because it avoids three weak positions:

1. It does not claim the whole AMR agent space is empty.
2. It does not compete directly with wet-lab antibiotic-design systems.
3. It does not require clinical decision-support validation, which would be hard to defend without clinical collaborators and a carefully approved rubric.

The original five-track idea is useful as a long-term roadmap, but it is too wide for a credible May 1 workshop submission. The May 1 paper should be:

- **Focused:** two benchmark tracks, not five.
- **Dry-lab only:** all tasks use public data, pinned tool versions, and reproducible scoring.
- **Evaluation-first:** the contribution is benchmark construction, baseline behavior, failure modes, and a disciplined AMR-specific evaluation rubric.
- **Honest:** the paper should document what agents can and cannot do on AMR reasoning, not imply that an in-silico system discovers clinically useful antibiotics.

The proposed submission should be a **benchmark plus critical evaluation** paper:

> AMR-Bench-mini evaluates whether tool-using language-model agents can synthesize evidence from bacterial genome assemblies, AMR databases, phenotype labels, and conflicting annotation outputs. We show that general agents can call tools and produce fluent rationales, but they struggle with versioned AMR ontologies, breakpoint-dependent phenotype labels, and cases where multiple databases disagree for legitimate biological or curation reasons.

This is a stronger and more reviewable paper than a broad agent system pitch.

---

## 2. Corrected Core Claims

This section is the guardrail for the final paper. Use these claims. Avoid the rejected claims.

### 2.1 Claims We Can Make

**Claim 1: Agentic biology has converged on a common architecture.**  
Planner/controller, tool router, domain tools, memory, critic/reviewer, optional self-evolution, and optional wet-lab loop appear repeatedly across systems such as Coscientist, ChemCrow, Biomni, STELLA, SAGA, The Virtual Lab, Robin, Google AI Co-scientist, and TxAgent.

**Claim 2: AMR is represented in resources and isolated benchmark items, but not as a dedicated agent benchmark.**  
Public AMR resources are rich: CARD/RGI, AMRFinderPlus, MEGARes, ResFinder, BV-BRC/PATRIC, CRyPTIC, PLSDB, AMPSphere, NCBI Pathogen Detection, and others. General bio/science benchmarks include isolated antibiotic or AMR-adjacent tasks. The gap is not "no AMR anywhere." The gap is "no dedicated AMR-specific multi-track agent benchmark with AMR-appropriate tasks, tool outputs, rubrics, and failure modes."

**Claim 3: Wet-lab antibiotic discovery is not the right competitive axis for this submission.**  
SAGA, Fleming, AMP-Designer, SPEL, SyntheMol-style work, The Virtual Lab, and Robin have much stronger wet-lab or lab-in-the-loop validation stories than we can produce under the current constraints. Our paper should not try to beat them. It should evaluate agentic AMR reasoning under reproducible dry-lab conditions.

**Claim 4: AMR reasoning has specific failure modes that generic bio-agent benchmarks do not isolate.**  
These include database-version drift, ambiguous gene-family calls, allele-level versus gene-family-level mismatches, phenotype labels that depend on testing standards and breakpoint versions, species-scoped tools, plasmid and mobile genetic element interpretation, and legitimate disagreement between databases.

**Claim 5: A small benchmark is acceptable if it is carefully specified.**  
A workshop paper does not need hundreds of tasks per track. A high-quality set of 50 to 100 total tasks, pinned tools, clear schemas, human-auditable evidence, and honest baseline analysis can be more convincing than a broad but under-specified benchmark.

### 2.2 Claims We Should Not Make

Do not claim:

- "All major bio-agent benchmarks have zero AMR coverage."
- "There is no AMR benchmark."
- "This is the first AMR benchmark."
- "This benchmark validates clinical treatment recommendations."
- "The agent discovers new antibiotics."
- "The agent resolves all AMR database disagreements."
- "Tool disagreement is always error."
- "CARD, AMRFinderPlus, MEGARes, ResFinder, and NDARO disagree on 10-30% of annotations" unless that percentage is generated by our own pilot and documented.
- "Google AI Co-scientist discovered a novel AMR mechanism" without the nuance that the system recapitulated an unpublished, experimentally validated AMR-relevant gene-transfer mechanism.
- "SAGA wet-lab validated antibiotic, nanobody, and DNA enhancer designs" without separating which tasks had wet-lab validation and which were computational/predictor-validated.
- "ApexAmphion has mouse-model validation" unless a source is found for that specific claim.

### 2.3 Safer Final-Paper Wording

Use this in the abstract or introduction:

> Although general bio-agent benchmarks contain isolated antibiotic or AMR-adjacent tasks, they do not provide a dedicated evaluation of agentic AMR reasoning across versioned databases, annotation tools, phenotype labels, and conflicting evidence. We introduce AMR-Bench-mini, a compact two-track benchmark for isolate-level AMR reasoning. The benchmark tests genotype-to-phenotype evidence synthesis and AMR database/tool-disagreement reconciliation using public bacterial genome assemblies, AST records, and pinned annotation outputs.

Use this for scope:

> AMR-Bench-mini is not a clinical decision-support benchmark and should not be used to recommend patient treatment. It evaluates evidence synthesis and tool use on retrospective public data.

Use this for the contribution:

> Our contribution is a reproducible task schema, a curated pilot dataset, pinned tool outputs, baseline agent results, and a taxonomy of AMR-specific agent failure modes.

---

## 3. Final Project Scope

### 3.1 In Scope for May 1

The May 1 project should include:

1. A benchmark definition document.
2. A small public pilot dataset.
3. Two benchmark tracks.
4. A reproducible evaluation harness.
5. At least two baseline systems.
6. A table of results.
7. A failure-mode taxonomy.
8. A short discussion of safety, biosecurity, and clinical non-use.
9. A paper draft that clearly distinguishes this work from wet-lab antibiotic discovery.

### 3.2 Out of Scope for May 1

The May 1 project should not include:

- A five-track benchmark.
- A public leaderboard.
- A clinical empiric-therapy agent.
- A novel-antibiotic generator.
- A resistance-evolution simulator.
- A metagenomic resistome mining benchmark.
- A claim of clinical usefulness.
- A claim of biological discovery.
- A benchmark requiring proprietary data.
- A benchmark requiring wet-lab validation.

### 3.3 Long-Term Extensions

The original five-track vision can appear as future work:

1. **GenoPheno:** genotype-to-phenotype evidence synthesis.
2. **DBReconcile:** database/tool-disagreement reconciliation.
3. **EmpiricRx:** guideline-consistency and stewardship-style reasoning from synthetic cases, explicitly not treatment recommendation.
4. **ResistomeMine:** metagenomic ARG/MGE discovery and prioritization.
5. **NovelAB-Triage:** antibiotic-design triage using public chemical and activity data.

Only the first two should be implemented for the submission.

---

## 4. Paper Thesis

### 4.1 One-Sentence Thesis

Agentic AMR research needs benchmarks that test evidence synthesis across public genomes, phenotypes, annotation tools, and database disagreements rather than only testing general biology QA or wet-lab antibiotic-design success.

### 4.2 One-Paragraph Thesis

Antimicrobial resistance is a natural stress test for biological agents because useful reasoning requires more than fluent biomedical text generation. An AMR agent must combine genome-derived evidence, phenotype labels, versioned databases, annotation-tool outputs, ontology-aware interpretation, and calibrated uncertainty. Existing general bio-agent benchmarks include isolated AMR or antibiotic-related examples, but they do not isolate these AMR-specific reasoning challenges. We therefore introduce AMR-Bench-mini, a compact two-track benchmark for isolate-level AMR reasoning. The benchmark evaluates genotype-to-phenotype evidence synthesis and database/tool-disagreement reconciliation on public data with pinned tool outputs and explicit safety constraints. Initial baselines show where general agents succeed, where they hallucinate, and where AMR-specific scaffolding is needed.

### 4.3 Reviewer-Facing Novelty

The novelty is not "AMR data exists." The novelty is:

- Agent-oriented task design for AMR.
- Explicit handling of conflicting annotation evidence.
- Versioned and auditable benchmark artifacts.
- AMR-specific error taxonomy.
- Dry-lab reproducibility.
- Safety-conscious framing that avoids clinical or wet-lab overclaims.

---

## 5. Current Local Assets

The local directory already contains a small BV-BRC-derived scaffold:

```text
amr-bench/
  data/
    ast.json
    metadata.json
    fasta/
      573.15595.fna
      573.15602.fna
      573.18476.fna
      573.18477.fna
      573.24245.fna
      573.24267.fna
      573.24349.fna
      573.24380.fna
      573.24386.fna
      573.24407.fna
  scripts/
    pull_fasta.py
    pull_isolates.py
```

The current scaffold contains:

- 10 *Klebsiella pneumoniae* isolates.
- 10 FASTA assemblies.
- 322 laboratory AST records.
- Metadata including strain, MLST when available, country, year, sequencing status, genome length, contig count, GC content, and host.
- AST panels across antibiotics including ceftriaxone, ceftazidime, cefepime, meropenem, ertapenem, ciprofloxacin, gentamicin, amikacin, trimethoprim/sulfamethoxazole, colistin, and others.

This is enough for a proof-of-concept, but not enough for the final benchmark if the paper wants credible evaluation. The benchmark should expand beyond 10 isolates or clearly label the current assets as a smoke-test subset.

### 5.1 Immediate Cleanup Needed

The scripts currently contain an absolute local root:

```text
/Users/ainergiz/iclr/amr-bench
```

Before release, replace this with a path derived from the script location, for example:

```python
ROOT = Path(__file__).resolve().parents[1]
```

Also add:

- `README.md`
- `requirements.txt` or `pyproject.toml`
- `data/README.md`
- `benchmark_schema.json`
- `LICENSE`
- `CITATION.cff` if time permits
- a clear data provenance file

---

## 6. Benchmark Tracks

The benchmark should have two tracks.

### 6.1 Track A: GenoPheno Evidence Synthesis

**Task name:** `genopheno`  
**Core question:** Given an isolate, AST context, species, antibiotic, and genome-derived evidence, can an agent predict or explain resistance phenotype using auditable evidence?

This is not just a raw prediction task. It should be framed as evidence synthesis:

- Identify relevant AMR genes or mutations.
- Map evidence to antibiotic class.
- Distinguish direct evidence from weak or indirect evidence.
- Produce a calibrated answer.
- Cite tool outputs and database entries.
- Avoid claiming certainty where phenotype labels or breakpoints are ambiguous.

#### 6.1.1 Inputs

Each task should provide:

- `task_id`
- `track = "genopheno"`
- `species`
- `genome_id`
- `genome_name`
- `assembly_path`
- `antibiotic`
- `antibiotic_class`
- `metadata`
- `available_evidence`
- optional `tool_outputs`
- optional `retrieved_database_snippets`

For closed-label evaluation, the visible input should not include the target phenotype. For rationale-only evaluation, the task can include the phenotype and ask the agent to explain it.

#### 6.1.2 Outputs

The agent should return structured JSON:

```json
{
  "task_id": "genopheno_kp_0001",
  "phenotype_prediction": "Resistant",
  "confidence": 0.78,
  "evidence": [
    {
      "type": "gene",
      "name": "blaCTX-M-like",
      "source": "AMRFinderPlus",
      "supports": "Resistant",
      "scope": "beta-lactam resistance"
    }
  ],
  "rationale": "Short evidence synthesis here.",
  "uncertainty": "Breakpoint and gene-family caveats here."
}
```

The benchmark harness should validate JSON syntax first, then score content.

#### 6.1.3 Labels

Labels come from laboratory AST records, but AST labels require careful handling:

- Keep the original `resistant_phenotype` field.
- Keep measurement, unit, sign, method, testing standard, and testing standard year where available.
- Do not collapse everything into binary labels without retaining provenance.
- Handle intermediate/non-susceptible labels explicitly if they appear.
- Pin whether the task uses the source label as-is or normalizes to binary.

For the paper, binary labels are acceptable for a pilot, but the data format should preserve richer AST metadata.

#### 6.1.4 Metrics

Primary metrics:

- Accuracy over phenotype labels.
- Macro-F1 if classes are imbalanced.
- Calibration error over confidence scores.
- JSON validity rate.
- Evidence citation validity.

Secondary metrics:

- Refusal or abstention rate.
- Rate of unsupported mechanistic claims.
- Rate of wrong antibiotic class mapping.
- Rate of hallucinated gene names.
- Rate of phenotype-label leakage if any labels accidentally appear in prompts.

#### 6.1.5 Human-Auditable Error Categories

For a small benchmark, human-auditable categories matter more than a single score:

- Correct phenotype, correct evidence.
- Correct phenotype, weak or wrong evidence.
- Wrong phenotype, plausible evidence.
- Wrong phenotype, hallucinated evidence.
- Tool call failure.
- Database-version confusion.
- Antibiotic-class confusion.
- Species/tool scope confusion.
- Overconfident answer despite ambiguous evidence.

### 6.2 Track B: DBReconcile

**Task name:** `dbreconcile`  
**Core question:** Given conflicting AMR annotations from multiple tools or databases for the same isolate, can an agent produce a calibrated reconciliation without pretending that disagreement always has a single correct answer?

This is the most distinctive track. It should be the paper's central contribution.

#### 6.2.1 Why This Track Matters

AMR annotation is not a single-source-of-truth problem. Different resources may disagree because of:

- Database version differences.
- Sequence identity and coverage thresholds.
- Allele-level versus gene-family-level reporting.
- Point mutation versus acquired gene focus.
- Species-specific rules.
- Ontology granularity.
- Different inclusion criteria for intrinsic resistance.
- Different treatment of partial genes, pseudogenes, contig boundaries, or low-quality assemblies.
- Different mappings from genes to drugs or drug classes.

A generic agent often treats all disagreement as a conflict to be "resolved." An AMR-aware agent should often say:

> These outputs are compatible at different ontology levels.

or:

> This disagreement is not resolvable from the provided evidence; additional sequence inspection or version-specific database review is required.

That makes the track scientifically meaningful.

#### 6.2.2 Inputs

Each task should provide:

- `task_id`
- `track = "dbreconcile"`
- `species`
- `genome_id`
- `assembly_path`
- `target_gene_or_drug_class`
- outputs from at least two tools or databases
- pinned tool versions
- pinned database versions
- optional AST label for downstream consistency check
- optional short database evidence snippets

The first version can use simulated or precomputed tool outputs if tool installation is not finished, but final paper claims should clearly distinguish real tool outputs from constructed examples.

#### 6.2.3 Outputs

The agent should return structured JSON:

```json
{
  "task_id": "dbrec_kp_0001",
  "reconciled_call": "Likely ESBL-associated beta-lactamase present",
  "confidence": 0.72,
  "disagreement_type": "ontology_granularity",
  "evidence_matrix": [
    {
      "source": "AMRFinderPlus",
      "reported_entity": "blaCTX-M-15",
      "supports_call": true
    },
    {
      "source": "CARD/RGI",
      "reported_entity": "CTX-M beta-lactamase family",
      "supports_call": true
    }
  ],
  "phenotype_consistency": "Consistent with ceftriaxone resistance, not sufficient alone for all beta-lactam calls.",
  "uncertainty": "Allele-level confirmation depends on thresholds and database versions."
}
```

#### 6.2.4 Disagreement Taxonomy

The benchmark should label disagreement types:

- `same_call_different_name`
- `gene_family_vs_allele`
- `threshold_difference`
- `database_version_difference`
- `drug_mapping_difference`
- `intrinsic_vs_acquired`
- `species_scope_difference`
- `point_mutation_vs_gene_presence`
- `partial_or_low_quality_hit`
- `true_conflict`
- `insufficient_evidence`

This taxonomy is likely to be one of the most useful paper artifacts.

#### 6.2.5 Metrics

Primary metrics:

- Correct disagreement-type classification.
- Correct reconciled call at the agreed ontology level.
- Evidence matrix completeness.
- Calibration quality.
- JSON validity.

Secondary metrics:

- Over-resolution rate: agent forces a single answer when the right answer is uncertainty.
- Under-resolution rate: agent refuses despite enough evidence.
- Hallucinated database fields.
- Unsupported literature claims.
- Version-awareness score.

#### 6.2.6 Why DBReconcile Can Be a Standalone Backup

If the two-track benchmark becomes too large, DBReconcile alone can become the paper:

> DBReconcile: Evaluating Agentic Reconciliation of Conflicting AMR Annotation Evidence

This would be narrower but still legitimate. It is the most feasible and most AMR-specific contribution.

---

## 7. Dataset Construction Plan

### 7.1 Target Dataset Size

For May 1:

- Minimum viable dataset: 30 total tasks.
- Good workshop dataset: 50 to 80 total tasks.
- Stretch dataset: 100 total tasks.

Recommended split:

- 30 to 50 `genopheno` tasks.
- 20 to 50 `dbreconcile` tasks.

Do not promise 50 to 200 tasks per track unless those tasks are actually built and checked.

### 7.2 Species Scope

The current local data is *Klebsiella pneumoniae*. That is a practical starting point because:

- It is a clinically important AMR pathogen.
- Many public isolates have AST records.
- AMR gene interpretation is rich enough to expose real reasoning issues.
- Existing tools such as Kleborate are useful for *Klebsiella*, while general tools such as AMRFinderPlus and RGI cover broader AMR calls.

However, there is a risk:

- A benchmark using only *Klebsiella pneumoniae* should not be described as a general AMR benchmark.

Safer wording:

> AMR-Bench-mini pilots our benchmark schema on *Klebsiella pneumoniae* isolates with public genome assemblies and laboratory AST records. The schema is species-general, but the submitted pilot focuses on one high-priority pathogen.

If time allows, add a small second species slice, but only if doing so does not weaken data quality.

### 7.3 Data Sources

Use public sources:

- BV-BRC/PATRIC for isolate metadata, genome assemblies, and AST records.
- CARD/RGI for resistance ontology and gene-family interpretation.
- AMRFinderPlus for NCBI production-style AMR annotation.
- MEGARes for alternative ARG hierarchy and database comparison.
- ResFinder if installation time allows.
- CRyPTIC only if adding a TB-specific extension, which is not recommended for May 1.

### 7.4 Data Provenance Requirements

Every task should retain:

- source URL or database name
- source access date
- source version if available
- genome ID
- assembly accession or local filename
- AST evidence field names
- testing standard and year where available
- tool name
- tool version
- database version
- command used to produce output

This is not optional. AMR resources change over time, and reviewers will notice if versioning is vague.

### 7.5 Data Cleaning Rules

Rules for AST records:

1. Preserve original labels.
2. Normalize antibiotic names into a controlled vocabulary.
3. Keep original antibiotic string as `antibiotic_raw`.
4. Keep measurement sign and unit.
5. Exclude records with missing phenotype labels from prediction scoring.
6. Do not mix CLSI and EUCAST interpretations without recording the standard.
7. Prefer tasks where the label is unambiguous.
8. Flag antibiotics with known species-specific caveats.

Rules for assemblies:

1. Check FASTA files are nonempty.
2. Record contig count and assembly status.
3. Flag highly fragmented assemblies.
4. Keep genome ID in every downstream artifact.

Rules for tool outputs:

1. Store raw output.
2. Store parsed output.
3. Keep tool command.
4. Keep version.
5. Do not manually edit raw tool outputs.

### 7.6 Candidate Task Selection

For `genopheno`, prioritize antibiotics where:

- multiple isolates have labels
- phenotype labels include both resistant and susceptible examples
- known AMR mechanisms are reasonably represented
- tool outputs are likely informative

From the current local scaffold, high-coverage antibiotics include:

- trimethoprim/sulfamethoxazole
- tobramycin
- meropenem
- gentamicin
- ciprofloxacin
- ceftriaxone
- ceftazidime
- ampicillin
- amoxicillin/clavulanic acid
- amikacin
- piperacillin/tazobactam
- cefepime

For `dbreconcile`, prioritize cases where:

- two tools report related but differently named entities
- one tool reports gene family while another reports allele
- one tool reports a hit and another does not
- one tool maps to antibiotic class and another maps to specific drugs
- AST phenotype provides a useful but not definitive consistency check

---

## 8. Toolchain Plan

### 8.1 Required Tools

Minimum:

- Python 3.10+
- jq for JSON inspection
- AMRFinderPlus
- CARD RGI if installable in time
- BLAST or DIAMOND if needed by annotation tools
- pandas or polars for dataset construction
- pytest for harness tests

Optional:

- ResFinder
- MEGARes plus AMR++/ResistomeAnalyzer-style pipeline
- Kleborate for *Klebsiella*-specific annotation

### 8.2 Tool Framing

Be precise in the paper:

- AMRFinderPlus is a callable NCBI AMR annotation tool.
- CARD is a database and ontology; RGI is the usual CARD annotation software.
- MEGARes is a database; execution typically goes through associated pipelines rather than "calling MEGARes" directly.
- NDARO is an NCBI AMR data/resource umbrella, not a standalone annotation tool in the same sense as AMRFinderPlus.
- Kleborate is useful but species-scoped, mainly for the *Klebsiella pneumoniae* species complex.

### 8.3 Pinned Output Strategy

For the paper, agents should not be required to install and run all AMR tools live during each evaluation. That makes the benchmark brittle and expensive.

Better:

1. Run tools once during benchmark construction.
2. Save raw outputs.
3. Save parsed outputs.
4. Give agents task-specific excerpts or file paths.
5. Score the structured answer.

This makes the benchmark reproducible and focused on reasoning rather than system administration.

### 8.4 Live-Tool Variant

As a stretch, include a live-tool setting:

- Agent receives FASTA and can call tool wrappers.
- Agent must decide which tools to call.
- Evaluation includes tool-call success and final answer.

This is useful but not necessary for the May 1 submission. The paper can define it as a future benchmark mode.

---

## 9. Agent Baselines

The paper needs baselines that are credible and runnable. Do not promise unavailable systems.

### 9.1 Baseline 1: No-Agent Tool Majority Baseline

This baseline uses parsed tool outputs with simple rules:

- For `genopheno`, predict resistant if any high-confidence gene or mutation maps to the antibiotic class.
- For `dbreconcile`, classify disagreement using simple name/family matching rules.

Purpose:

- Establish that some tasks are solvable without an LLM.
- Reveal where agent reasoning adds value or fails.

### 9.2 Baseline 2: Generic ReAct LLM Agent

This baseline uses a frontier model with:

- task prompt
- access to provided files
- optional retrieval over database snippets
- structured JSON output requirement

Purpose:

- Test generic agent behavior.
- Measure hallucination, JSON validity, overconfidence, and evidence synthesis.

### 9.3 Baseline 3: AMR-Scaffolded Agent

This is the main methods-ish baseline:

- Same model as Baseline 2.
- Adds AMR-specific instructions.
- Adds controlled ontology hints.
- Requires evidence matrix.
- Requires explicit uncertainty.
- Uses a disagreement taxonomy.
- Forbids clinical recommendations.

Purpose:

- Show that AMR-specific scaffolding improves reasoning quality.
- Make the paper more than a dataset announcement.

### 9.4 Optional Baseline 4: Biomni or Another Bio-Agent

Only include if runnable quickly and fairly.

Risks:

- Installation may be time-consuming.
- Tool dependencies may not match the benchmark.
- It may be hard to ensure fair prompting.

Safe wording:

> We include a general biomedical agent baseline where available; when a system could not be run reproducibly under our constraints, we compare against a generic ReAct agent and an AMR-scaffolded variant using the same base model.

### 9.5 Do Not Promise These Baselines

Do not promise:

- Google AI Co-scientist, unless we have actual access.
- The Virtual Lab as a runnable baseline, unless adapting its public code is actually done.
- SAGA, unless code and exact setup are available.
- Robin, unless the benchmark task aligns with its released capabilities.

The paper can cite these systems as landscape context, not as evaluated baselines.

---

## 10. Evaluation Harness

### 10.1 Harness Responsibilities

The harness should:

1. Load tasks from JSONL.
2. Validate task schema.
3. Call a baseline runner.
4. Capture raw model output.
5. Parse structured JSON.
6. Score automatic fields.
7. Emit per-task results.
8. Emit aggregate metrics.
9. Save failures for manual review.

### 10.2 Suggested File Layout

```text
amr-bench/
  README.md
  pyproject.toml
  data/
    README.md
    raw/
    interim/
    processed/
    tasks/
      genopheno.jsonl
      dbreconcile.jsonl
    tool_outputs/
      amrfinderplus/
      rgi/
      megares/
      resfinder/
    fasta/
    ast.json
    metadata.json
  scripts/
    pull_isolates.py
    pull_fasta.py
    build_tasks.py
    run_amrfinderplus.py
    run_rgi.py
    parse_tool_outputs.py
  src/
    amr_bench/
      __init__.py
      schema.py
      scoring.py
      baselines.py
      prompts.py
      runners.py
  tests/
    test_schema.py
    test_scoring.py
    test_fixtures.py
  results/
    baseline_tool_majority.jsonl
    baseline_react.jsonl
    baseline_amr_scaffold.jsonl
```

This is more structure than the submission strictly needs, but it keeps the execution clean.

### 10.3 Task Schema

Each JSONL row should be self-contained:

```json
{
  "task_id": "genopheno_kp_000001",
  "track": "genopheno",
  "species": "Klebsiella pneumoniae",
  "genome_id": "573.18477",
  "genome_name": "Klebsiella pneumoniae strain CCUG 70747",
  "antibiotic": "ceftriaxone",
  "antibiotic_class": "third-generation cephalosporin",
  "assembly_path": "data/fasta/573.18477.fna",
  "metadata": {
    "collection_year": 2013,
    "isolation_country": "Sweden",
    "sequencing_status": "Complete",
    "contigs": 4
  },
  "visible_evidence": {
    "tool_outputs": [],
    "database_snippets": []
  },
  "gold": {
    "phenotype": "Resistant",
    "measurement": ">32",
    "measurement_unit": "mg/L",
    "testing_standard": "EUCAST"
  }
}
```

For held-out task release, either remove `gold` from the public prompt or keep gold in a separate file.

### 10.4 Output Schema

Agent outputs should conform to:

```json
{
  "task_id": "string",
  "answer": "string",
  "confidence": 0.0,
  "evidence": [
    {
      "source": "string",
      "claim": "string",
      "supports_answer": true
    }
  ],
  "rationale": "string",
  "uncertainty": "string"
}
```

Track-specific fields can extend this schema.

### 10.5 Scoring Rules

Use three layers:

1. **Format scoring:** valid JSON, required keys present, confidence in range.
2. **Automatic task scoring:** prediction accuracy, disagreement-type accuracy, evidence-source matching.
3. **Manual audit scoring:** unsupported claims, hallucinated genes, wrong database interpretation.

The paper can report manual audit on a sample if full manual labeling is too slow.

### 10.6 Score Reporting

Tables should include:

- number of tasks
- JSON validity
- answer accuracy
- evidence validity
- calibration error
- unsupported-claim rate
- overconfidence rate

For example:

```text
Model                 JSON valid   Accuracy   Evidence valid   Unsupported claims   ECE
Tool majority         1.00         0.xx       0.xx             n/a                  n/a
Generic ReAct         0.xx         0.xx       0.xx             0.xx                 0.xx
AMR-scaffolded ReAct  0.xx         0.xx       0.xx             0.xx                 0.xx
```

Do not invent numbers. Leave placeholders until the runs are completed.

---

## 11. Prompting Plan

### 11.1 Generic ReAct Prompt

The generic prompt should be simple:

```text
You are a biomedical research assistant. Solve the AMR benchmark task using only the provided evidence. Return valid JSON matching the requested schema. If the evidence is insufficient, say so and lower your confidence.
```

### 11.2 AMR-Scaffolded Prompt

The AMR-specific prompt should encode the benchmark's scientific assumptions:

```text
You are evaluating retrospective antimicrobial-resistance evidence for a benchmark. This is not a clinical treatment task. Use only provided genome metadata, AST records, and annotation evidence.

Rules:
- Keep database and tool versions explicit when available.
- Do not assume that database disagreement means one source is wrong.
- Distinguish gene-family, allele-level, mutation-level, and drug-class evidence.
- Distinguish intrinsic and acquired resistance when evidence allows.
- Do not invent AMR genes, mutations, breakpoints, papers, or tool outputs.
- If evidence is insufficient, report uncertainty.
- Return valid JSON only.
```

### 11.3 DBReconcile-Specific Prompt Additions

```text
Classify the disagreement type using exactly one of:
same_call_different_name, gene_family_vs_allele, threshold_difference,
database_version_difference, drug_mapping_difference, intrinsic_vs_acquired,
species_scope_difference, point_mutation_vs_gene_presence, partial_or_low_quality_hit,
true_conflict, insufficient_evidence.

Your reconciled call may be "not resolvable from provided evidence" if that is the most accurate answer.
```

### 11.4 GenoPheno-Specific Prompt Additions

```text
Predict the AST phenotype only as Resistant, Susceptible, Intermediate, Non-susceptible, or Insufficient evidence. Explain which evidence supports or weakens the prediction. Do not use patient-treatment language.
```

---

## 12. Experiments

### 12.1 Minimal Experiment Set

To submit a credible paper, run:

1. Tool-majority baseline on all tasks.
2. Generic ReAct baseline on all tasks.
3. AMR-scaffolded ReAct baseline on all tasks.
4. Manual audit on at least 20 model outputs.

### 12.2 Ablations

If time allows:

- Generic prompt versus AMR-scaffolded prompt.
- With versus without database snippets.
- With versus without evidence-matrix requirement.
- Free-form output versus structured JSON.
- Confidence required versus no confidence required.

### 12.3 Expected Result Shape

The likely publishable result is:

- AMR-scaffolded agent improves JSON validity and evidence quality.
- Generic agent often produces plausible but unsupported rationales.
- Database reconciliation remains hard even when final phenotype prediction is correct.
- Confidence is poorly calibrated without explicit uncertainty prompting.
- Some disagreements cannot be resolved from benchmark evidence and should not be forced.

Even if accuracy gains are modest, the paper can still be useful if the failure analysis is strong.

### 12.4 Failure Analysis Targets

Audit for:

- hallucinated AMR genes
- hallucinated citations
- wrong antibiotic class
- treating CARD/RGI, AMRFinderPlus, MEGARes, ResFinder, and NDARO as interchangeable
- ignoring tool versions
- claiming clinical treatment implications
- over-interpreting susceptible phenotypes
- using AST labels as if they were mechanism labels
- ignoring species scope of Kleborate
- resolving legitimate ontology granularity differences as conflicts

---

## 13. Paper Outline

### 13.1 Four-Page Version

Use a compact paper structure:

1. **Introduction**
   - Agentic biology is moving fast.
   - AMR is a high-stakes domain with rich public data.
   - General benchmarks do not isolate AMR-specific agent reasoning.
   - We introduce AMR-Bench-mini.

2. **Related Work**
   - Agentic bio systems.
   - AMR resources and annotation tools.
   - Bio/science-agent benchmarks.
   - Wet-lab antibiotic discovery systems, framed as complementary.

3. **Benchmark**
   - Task tracks.
   - Data sources.
   - Schema.
   - Metrics.
   - Safety boundaries.

4. **Baselines and Results**
   - Tool baseline.
   - Generic ReAct.
   - AMR-scaffolded ReAct.
   - Aggregate table.
   - Failure-mode table.

5. **Discussion**
   - What agents can do.
   - What agents get wrong.
   - Why AMR-specific evaluation matters.
   - Limitations and future tracks.

### 13.2 Nine-Page Version

If the venue permits a longer paper and enough experiments are complete:

1. Introduction
2. Related Work
3. Benchmark Design Principles
4. Data and Task Construction
5. Track A: GenoPheno
6. Track B: DBReconcile
7. Baseline Agents
8. Results
9. Failure Analysis
10. Safety and Biosecurity
11. Limitations
12. Future Work

Do not expand scope just because the page limit allows it. Use extra pages for detail, examples, and error analysis.

---

## 14. Related Work Positioning

### 14.1 Agentic Biology Systems

Mention:

- Coscientist: autonomous chemical research with LLM modules and lab automation integration.
- ChemCrow: LLM plus chemistry tools.
- Biomni: general biomedical agent with many tools and databases.
- STELLA: self-evolving toolset and biomedical evaluation, but avoid unsupported "multimodal eval" claims.
- SAGA: objective-evolving agent with wet-lab validation for an *E. coli* antibiotic hit and PD-L1 binders; do not overstate DNA enhancer validation.
- Google AI Co-scientist: generate-debate-evolve style system that recapitulated an unpublished experimentally validated AMR-relevant gene-transfer mechanism.
- The Virtual Lab: multi-agent scientific collaboration with experimental nanobody validation.
- Robin: autonomous dry-lab/wet-lab loop for disease-related drug discovery.
- TxAgent: therapeutic reasoning agent with many biomedical tools.

Position:

> These systems motivate agentic scientific workflows, but AMR-specific evaluation remains underdeveloped.

### 14.2 Antibiotic and AMP Discovery

Mention:

- Fleming for Mtb antibiotic design; report the 5/6 confirmed predicted inhibitors caveat carefully.
- AMP-Designer and SPEL for stronger experimental validation.
- ApexAmphion for in vitro/mechanistic AMP work, not mouse validation unless verified.
- SyntheMol/SyntheMol-RL and classic AI-antibiotic discovery work as non-agentic or generator-focused anchors.

Position:

> These systems address molecule generation and experimental validation. AMR-Bench-mini instead evaluates retrospective evidence synthesis and annotation reasoning.

### 14.3 Benchmarks

Mention:

- LAB-Bench
- BixBench
- Biomni-Eval1
- ScienceAgentBench
- MLAgentBench/MLE-bench
- BioPlanner/BioProBench
- WMDP-Bio and other safety benchmarks if relevant

Position:

> General science and biology benchmarks are useful but do not provide a dedicated AMR benchmark with versioned annotation outputs, AST evidence, and disagreement-aware scoring.

### 14.4 AMR Resources

Mention:

- CARD/RGI/ARO
- AMRFinderPlus
- MEGARes
- ResFinder
- BV-BRC/PATRIC
- CRyPTIC
- PLSDB
- AMPSphere

Be precise:

- CARD current site count versus NAR 2023 paper count must not be mixed.
- BV-BRC 67,817 AST genomes is the 2021 paper scale; current materials may report larger counts.
- CRyPTIC 12,289 quality-matched MTB isolates is a precise compendium count; larger TB catalogues are separate.

---

## 15. Safety and Biosecurity Framing

### 15.1 What the Benchmark Does Not Enable

State clearly:

- The benchmark does not provide protocols for engineering resistance.
- The benchmark does not optimize pathogens.
- The benchmark does not recommend patient therapy.
- The benchmark does not design deployable antibiotics.
- The benchmark does not include wet-lab instructions.

### 15.2 What the Benchmark Does Enable

It enables:

- safer evaluation of retrospective evidence synthesis
- identification of hallucination and overconfidence
- reproducible comparison of agents on AMR-specific reasoning
- better understanding of database/tool disagreement

### 15.3 Guardrails

Implement:

- No clinical advice prompts.
- No wet-lab protocol generation.
- No optimization of resistance acquisition.
- No instructions for evading detection or increasing pathogenicity.
- Prompts explicitly state retrospective benchmark use.
- Outputs penalize treatment recommendations and unsupported actionable claims.

### 15.4 Paper Wording

Use:

> Because AMR reasoning can intersect with clinical and biosecurity-sensitive contexts, AMR-Bench-mini is designed as a retrospective evidence-synthesis benchmark. It excludes treatment recommendation, pathogen engineering, and wet-lab protocol tasks.

---

## 16. Execution Timeline

The deadline is tight. The plan should be run as a focused sprint.

### Day 0: 2026-04-25

Goal:

- Freeze the scope.
- Stop expanding tracks.
- Create plan and task list.

Tasks:

- Confirm two-track benchmark.
- Create this execution document.
- Create or update repo README.
- Parameterize existing scripts.
- Inventory current data.
- Decide whether to expand beyond 10 isolates.

Deliverable:

- Final scope statement.
- Local execution plan.

### Day 1: 2026-04-26

Goal:

- Build the dataset skeleton.

Tasks:

- Clean current BV-BRC pull scripts.
- Add reproducible data provenance files.
- Build JSONL task schema.
- Convert current AST and metadata into initial `genopheno` tasks.
- Select antibiotics with enough labels.
- Define `dbreconcile` task schema.
- Create 5 hand-checked example tasks for each track.

Deliverable:

- `data/tasks/genopheno.jsonl`
- `data/tasks/dbreconcile.jsonl`
- schema validation tests

Decision gate:

- If tool installation looks risky, use pinned/precomputed example outputs for the initial DBReconcile tasks and clearly label them.

### Day 2: 2026-04-27

Goal:

- Produce or simulate pinned tool outputs.

Tasks:

- Install/run AMRFinderPlus if feasible.
- Install/run RGI if feasible.
- Parse outputs into normalized evidence records.
- If MEGARes/ResFinder are too slow, include them only in related work or future work.
- Expand task count to 30+.
- Implement scoring functions.

Deliverable:

- parsed tool outputs
- first scored tool-majority baseline
- reproducible commands

Decision gate:

- If less than 30 high-quality tasks exist by end of day, switch paper to DBReconcile-focused submission.

### Day 3: 2026-04-28

Goal:

- Run agent baselines.

Tasks:

- Implement generic ReAct runner.
- Implement AMR-scaffolded runner.
- Run both on all tasks.
- Save raw model outputs.
- Score JSON validity and automatic metrics.
- Begin manual audit.

Deliverable:

- `results/baseline_react.jsonl`
- `results/baseline_amr_scaffold.jsonl`
- first result table

Decision gate:

- If agent runs are unstable, reduce task count but keep all outputs auditable.

### Day 4: 2026-04-29

Goal:

- Complete analysis and write the paper.

Tasks:

- Finish manual audit.
- Build aggregate tables.
- Build failure-mode taxonomy table.
- Draft paper sections.
- Add benchmark examples.
- Write limitations honestly.
- Make source claims precise.

Deliverable:

- complete paper draft
- complete result tables
- complete related work section

### Day 5: 2026-04-30

Goal:

- Polish and de-risk.

Tasks:

- Verify every strong factual claim.
- Remove unsupported "first" claims.
- Check all sources.
- Check figures and tables.
- Ensure no clinical-overclaim language.
- Ensure dataset and code links are present or marked "to be released."
- Run harness tests.
- Render final PDF.

Deliverable:

- submission-ready PDF
- clean abstract
- clean camera-ready style source

### Day 6: 2026-05-01

Goal:

- Submit.

Tasks:

- Final read for scope drift.
- Confirm deadline timezone.
- Upload PDF.
- Upload supplementary links if allowed.
- Archive exact code/data state.

Deliverable:

- submitted paper
- frozen benchmark artifact

---

## 17. Concrete Engineering Tasks

### 17.1 Repository Hygiene

Tasks:

- Replace absolute paths in scripts.
- Create package structure.
- Add README with quickstart.
- Add data provenance file.
- Add requirements file.
- Add schema tests.
- Add result directories.

Acceptance criteria:

- A fresh user can run data-processing scripts from the repository root.
- No script depends on `/Users/ainergiz/...`.
- Existing data files are not silently overwritten without an explicit flag.

### 17.2 Data Builder

Build `scripts/build_tasks.py`.

Inputs:

- `data/metadata.json`
- `data/ast.json`
- `data/fasta/*.fna`
- optional parsed tool outputs

Outputs:

- `data/tasks/genopheno.jsonl`
- `data/tasks/dbreconcile.jsonl`

Acceptance criteria:

- Deterministic output order.
- Stable task IDs.
- Valid JSONL.
- Schema validation passes.
- Every task includes source provenance.

### 17.3 Schema Validator

Build `src/amr_bench/schema.py`.

Responsibilities:

- Validate task rows.
- Validate model outputs.
- Fail with clear error messages.

Acceptance criteria:

- Invalid rows produce actionable errors.
- Tests cover missing fields and wrong types.

### 17.4 Scoring

Build `src/amr_bench/scoring.py`.

Responsibilities:

- score phenotype prediction
- score disagreement type
- score JSON validity
- score confidence range
- score evidence source matching

Acceptance criteria:

- Unit tests for each score.
- Aggregate metrics emitted as JSON and Markdown.

### 17.5 Baselines

Build `src/amr_bench/baselines.py`.

Baselines:

- tool-majority or evidence-rule baseline
- generic LLM baseline
- AMR-scaffolded LLM baseline

Acceptance criteria:

- All baselines write raw outputs.
- All baselines can be re-scored without rerunning model calls.
- Failed model calls are captured, not dropped.

### 17.6 Manual Audit Sheet

Create `results/manual_audit.tsv`.

Fields:

- task_id
- model
- answer_correct
- evidence_valid
- hallucinated_gene
- hallucinated_source
- wrong_antibiotic_class
- overconfident
- clinical_overclaim
- notes

Acceptance criteria:

- At least 20 audited outputs.
- Error taxonomy table can be generated from it.

---

## 18. Figures and Tables

### 18.1 Figure 1: Benchmark Schematic

Show:

- isolate genome and AST record
- annotation tools/databases
- task generator
- agent
- structured output
- scoring

This can be a simple diagram.

### 18.2 Table 1: Benchmark Tracks

Columns:

- Track
- Input
- Output
- Metric
- AMR-specific challenge

Rows:

- GenoPheno
- DBReconcile

### 18.3 Table 2: Dataset Summary

Columns:

- Species
- Isolates
- AST records
- Antibiotics
- Tasks
- Tool outputs

### 18.4 Table 3: Baseline Results

Columns:

- Baseline
- JSON validity
- Accuracy or disagreement accuracy
- Evidence validity
- Unsupported-claim rate
- Calibration

### 18.5 Table 4: Failure Modes

Columns:

- Failure mode
- Example
- Why it matters
- Affected baseline

### 18.6 Appendix Table: Source Versions

Columns:

- Resource/tool
- Version/date
- Role in benchmark
- URL

---

## 19. Limitations

The paper should state these limitations plainly:

1. The pilot focuses on a small number of public isolates.
2. If only *Klebsiella pneumoniae* is used, species generality is not demonstrated.
3. AST labels are retrospective and may depend on testing standards and breakpoint versions.
4. Genotype-to-phenotype prediction is not equivalent to clinical treatment recommendation.
5. Database disagreement is not always error.
6. Tool versions and database versions affect results.
7. LLM baseline performance may vary by prompt and model release.
8. The benchmark does not validate novel antibiotic discovery.
9. Manual audit is limited by available expertise and time.
10. Some AMR mechanisms may require evidence not present in short-read assemblies or current annotation outputs.

This limitation section is a strength, not a weakness. GenBio reviewers are likely to respect careful boundaries.

---

## 20. Risk Register

### Risk 1: Benchmark Claim Too Broad

Failure mode:

- Reviewers find AMR examples in general benchmarks and reject the "no AMR coverage" claim.

Mitigation:

- Use the narrowed claim: no dedicated AMR-specific multi-track agent benchmark.

### Risk 2: Dataset Too Small

Failure mode:

- Reviewers see 10 isolates and call it a toy.

Mitigation:

- Expand task count if possible.
- Frame as benchmark schema plus pilot.
- Emphasize auditable task quality.
- Include future expansion plan.

### Risk 3: Tool Installation Consumes the Sprint

Failure mode:

- AMRFinderPlus/RGI/ResFinder installation takes too long.

Mitigation:

- Use one production tool plus curated examples for first submission.
- Clearly state which outputs are from live tools and which are constructed evidence examples.
- Do not claim full multi-tool execution unless done.

### Risk 4: Clinical Overclaim

Failure mode:

- Paper sounds like treatment recommendation without clinical validation.

Mitigation:

- Exclude EmpiricRx from May 1.
- Use retrospective evidence-synthesis language.
- Add explicit non-clinical-use statement.

### Risk 5: Unsupported Literature Claims

Failure mode:

- Paper repeats errors from the initial lit review.

Mitigation:

- Use the corrected claim list in this document.
- Verify each strong claim before submission.

### Risk 6: Baseline Results Are Weak

Failure mode:

- AMR-scaffolded prompt does not improve accuracy.

Mitigation:

- Report evidence validity, unsupported-claim rate, and calibration, not only accuracy.
- Emphasize failure modes and benchmark need.

### Risk 7: Data Leakage

Failure mode:

- Model memorized public isolate data or labels.

Mitigation:

- Treat this as retrospective benchmark limitation.
- Include tasks where reasoning over provided evidence matters more than raw memorization.
- If possible, select less prominent isolates or construct tasks around tool-output reconciliation.

---

## 21. Submission Abstract Draft

Draft:

> Agentic systems are increasingly used for biological discovery, but antimicrobial resistance (AMR) exposes evaluation challenges that are not captured by general bio-agent benchmarks: versioned databases, conflicting annotation tools, phenotype labels tied to testing standards, and uncertainty about how genotype evidence maps to drug resistance. We introduce AMR-Bench-mini, a compact benchmark for agentic AMR reasoning over public bacterial genome assemblies, laboratory AST records, and pinned annotation evidence. The benchmark contains two tracks: genotype-to-phenotype evidence synthesis and database/tool-disagreement reconciliation. We evaluate a rule-based tool baseline, a generic tool-using language-model agent, and an AMR-scaffolded agent that is required to produce structured evidence matrices and calibrated uncertainty. Our analysis highlights AMR-specific failure modes including hallucinated resistance genes, ontology-level confusion, unsupported phenotype rationales, and over-resolution of legitimate database disagreement. AMR-Bench-mini is designed as a retrospective evidence-synthesis benchmark, not a clinical decision-support system, and provides a reproducible starting point for safer evaluation of biological agents in AMR.

This abstract should be edited after results exist.

---

## 22. Introduction Draft Skeleton

Paragraph 1:

- Agentic biological systems now combine LLM planners with tools, critics, and sometimes wet-lab loops.
- Cite Coscientist, ChemCrow, Biomni, SAGA, Virtual Lab, Robin, Google AI Co-scientist.

Paragraph 2:

- AMR is a compelling domain because it is high impact and data rich.
- Public resources include AMR databases, annotation tools, genome assemblies, and AST records.
- But AMR reasoning is hard because evidence is fragmented, versioned, and sometimes contradictory.

Paragraph 3:

- Existing general benchmarks evaluate broad biology, bioinformatics, or science-agent capabilities.
- They contain isolated AMR or antibiotic items but do not evaluate AMR as a coherent agentic reasoning problem.

Paragraph 4:

- Introduce AMR-Bench-mini.
- Two tracks.
- Contributions.

Contribution bullets:

- A task schema for retrospective AMR agent evaluation.
- A pilot dataset from public isolate genomes and AST records.
- A database/tool-disagreement taxonomy.
- Baseline results and failure analysis.
- Safety boundaries for non-clinical use.

---

## 23. Methods Draft Skeleton

### 23.1 Data Sources

Describe:

- BV-BRC/PATRIC isolate metadata, genome assemblies, and AST records.
- AMRFinderPlus and/or CARD/RGI outputs if generated.
- Any curated database snippets.

Include:

- access date
- versions
- species
- isolate count
- AST record count
- antibiotics

### 23.2 Task Generation

Describe:

- filtering criteria
- phenotype label handling
- antibiotic normalization
- task ID generation
- train/dev/test or public/held-out split, if any

### 23.3 Track Definitions

Define:

- GenoPheno
- DBReconcile

### 23.4 Baselines

Describe:

- rule baseline
- generic ReAct agent
- AMR-scaffolded ReAct agent

### 23.5 Metrics

Describe:

- format validity
- prediction accuracy
- disagreement classification accuracy
- evidence validity
- unsupported-claim rate
- calibration

### 23.6 Manual Audit

Describe:

- audit sample size
- audit fields
- how disagreements were handled

---

## 24. Results Draft Skeleton

### 24.1 Benchmark Summary

Report:

- number of isolates
- number of AST records
- number of antibiotics
- number of tasks
- number of disagreement cases

### 24.2 Baseline Performance

Report:

- table by track
- table by model
- JSON validity
- accuracy
- evidence validity

### 24.3 Failure Modes

Discuss:

- hallucinated genes
- wrong ontology level
- overconfident uncertainty
- clinical overclaim
- database version confusion
- forced resolution of legitimate disagreement

### 24.4 Case Studies

Include 2 to 3 compact examples:

1. A straightforward resistant case where all tools agree.
2. A case where phenotype and annotation evidence conflict.
3. A DBReconcile case where two tools are compatible at different ontology levels.

---

## 25. Discussion Draft Skeleton

Key points:

- AMR-specific reasoning should be evaluated directly.
- Tool use alone does not guarantee correct evidence synthesis.
- Structured evidence matrices help.
- Uncertainty is scientifically appropriate in many AMR cases.
- Benchmark expansion should add more species, more tools, and carefully designed stewardship-style tasks.

Avoid:

- claiming clinical readiness
- claiming discovery
- claiming general AMR coverage from one species

---

## 26. Source and Fact Checklist

Before submission, verify these exact claims:

### 26.1 GenBio

- Deadline: 2026-05-01 AOE.
- Wengong Jin is listed as an organizer.
- Yusuf Roohani is listed as an invited speaker, not organizer.
- James Zou is listed as an invited speaker.

Source:

- https://genbio-workshop.github.io/2026/

### 26.2 SAGA

Allowed:

- SAGA is an objective-evolving agentic system.
- Wengong Jin is an author.
- It reports wet-lab validation for an *E. coli* antibiotic hit.
- It reports wet-lab validation for PD-L1 nanobody binders.

Avoid:

- saying DNA enhancers were wet-lab validated unless verified.

Source:

- https://arxiv.org/abs/2512.21782

### 26.3 Google AI Co-scientist

Allowed:

- Multi-agent Gemini-based system.
- Recapitulated an unpublished experimentally validated AMR-relevant gene-transfer mechanism.

Avoid:

- saying simply "discovered novel AMR mechanism" without nuance.

Source:

- https://arxiv.org/abs/2502.18864

### 26.4 STELLA

Allowed:

- Self-evolving toolset.
- Reports results on HLE: Biomedicine and LAB-Bench DBQA/LitQA.

Avoid:

- "beat Biomni on multimodal eval" unless a source is found.
- conflating Ruofan Jin with Wengong Jin.

Source:

- https://arxiv.org/abs/2507.02004

### 26.5 AMP and Antibiotic Systems

Allowed:

- AMP-Designer and SPEL have stronger animal/in vivo validation claims.
- ApexAmphion has in vitro/mechanistic validation unless new source verifies mouse data.
- Fleming reports 5/6 predicted inhibitors confirmed in vitro, not 83% of all screened molecules.

Sources:

- https://pubmed.ncbi.nlm.nih.gov/40043127/
- https://www.nature.com/articles/s41564-025-02114-4
- https://pubmed.ncbi.nlm.nih.gov/41040195/
- https://sciety.org/articles/activity/10.1101/2025.04.01.646719

### 26.6 AMR Resources

Allowed:

- CARD current website and CARD NAR 2023 paper may report different counts; cite version-specific counts.
- MEGARes 3.0 reports 8,733 accessions.
- BV-BRC/PATRIC 2021 paper supports 67,817 bacterial genomes with AST data; current BV-BRC material may report larger counts.
- CRyPTIC compendium: 12,289 quality-matched MTB isolates with WGS and quantitative DST.
- PLSDB 2025: 72,360 plasmids.
- AMPSphere: 863,498 candidate AMPs from 87,920 prokaryotic genomes and 63,410 metagenomes.

Sources:

- https://card.mcmaster.ca/
- https://academic.oup.com/nar/article/51/D1/D690/6764414
- https://academic.oup.com/nar/article/51/D1/D744/6830666
- https://academic.oup.com/bib/article/22/6/bbab313/6347947
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8901960/
- https://academic.oup.com/nar/article/53/D1/D189/7905312
- https://pubmed.ncbi.nlm.nih.gov/38843834/

### 26.7 Benchmarks

Allowed:

- General benchmarks include isolated AMR or antibiotic-related items.
- They do not appear to provide a dedicated AMR-specific multi-track agent benchmark.

Avoid:

- "zero AMR coverage."

Sources:

- https://huggingface.co/datasets/futurehouse/lab-bench
- https://huggingface.co/datasets/futurehouse/BixBench
- https://huggingface.co/datasets/osunlp/ScienceAgentBench

---

## 27. Final Recommendation

Submit the paper as:

> AMR-Bench-mini: A Focused Benchmark for Agentic Antimicrobial Resistance Reasoning

Implement:

- GenoPheno
- DBReconcile
- rule baseline
- generic ReAct baseline
- AMR-scaffolded ReAct baseline
- failure-mode taxonomy
- strict safety boundaries

Do not implement for this submission:

- EmpiricRx
- ResistomeMine
- NovelAB-Triage
- resistance-evolution adversary
- wet-lab antibiotic design
- clinical recommendations

The paper should argue that AMR is not just another biomedical QA topic. It is a domain where agents must handle versioned tools, phenotype uncertainty, ontology mismatches, and legitimate disagreement. That is the reviewable contribution.

---

## 28. Next Action Checklist

Immediate next actions:

- [ ] Rename or create `amr-bench/README.md` with this narrowed scope.
- [ ] Fix absolute paths in `amr-bench/scripts/*.py`.
- [ ] Create `data/tasks/` directory.
- [ ] Create `scripts/build_tasks.py`.
- [ ] Create schema validator.
- [ ] Generate first `genopheno.jsonl`.
- [ ] Define 10 hand-checked `dbreconcile` examples.
- [ ] Decide whether AMRFinderPlus/RGI can be installed in time.
- [ ] Run rule baseline.
- [ ] Run generic LLM baseline.
- [ ] Run AMR-scaffolded LLM baseline.
- [ ] Fill results table.
- [ ] Write paper draft.
- [ ] Remove unsupported claims from the older lit-review document before using it as paper source material.

The most important discipline is scope control. A finished two-track benchmark is a paper. An unfinished five-track benchmark is only an idea.
