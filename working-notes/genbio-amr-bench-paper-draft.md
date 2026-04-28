# AMR-Bench-mini: A Focused Benchmark for Agentic Antimicrobial Resistance Reasoning

**Status:** working draft from the current local pilot  
**Generated:** 2026-04-25  
**Code/data scaffold:** `amr-bench/`  
**Clinical status:** retrospective benchmark only; not clinical decision support  

## Abstract

Agentic systems are increasingly used for biological discovery, but antimicrobial
resistance (AMR) exposes evaluation challenges that are not captured by general
bio-agent benchmarks: versioned databases, conflicting annotation tools,
phenotype labels tied to testing standards, and uncertainty about how genotype
evidence maps to drug resistance. We introduce AMR-Bench-mini, a compact pilot
benchmark for agentic AMR reasoning over public bacterial genome assemblies,
laboratory AST records, and pinned annotation evidence. The benchmark contains
two tracks: genotype-to-phenotype evidence synthesis and database/tool
disagreement reconciliation. In the current pilot, AMR-Bench-mini contains 212
GenoPheno tasks and 150 DBReconcile tasks over 10 public *Klebsiella pneumoniae*
isolates. A deterministic rule baseline achieves 74.53% accuracy on GenoPheno
and 100.00% on the current heuristic DBReconcile labels, highlighting both the
utility and the current limitations of this pilot: the DBReconcile labels must
be manually audited before they can be treated as publication-grade gold labels.
AMR-Bench-mini is designed as a retrospective evidence-synthesis benchmark, not
a clinical decision-support system, and provides a reproducible starting point
for safer evaluation of biological agents in AMR.

## 1. Introduction

Agentic biological research systems have converged on a recognizable workflow:
a planner or controller routes work through domain tools, stores intermediate
results, and uses a critic or reviewer loop to refine candidate answers. Systems
such as Coscientist, ChemCrow, Biomni, STELLA, SAGA, The Virtual Lab, Robin,
Google AI Co-scientist, and TxAgent show that this design pattern is becoming a
standard way to organize language models for scientific work.

AMR is a useful stress test for these systems because it is both data-rich and
scientifically unforgiving. A plausible AMR answer often requires more than a
fluent explanation. It requires matching genome-derived evidence to a drug or
drug class, understanding the scope of annotation tools, respecting database and
breakpoint versioning, and knowing when apparently conflicting outputs are
compatible at different ontology levels.

General biology and science-agent benchmarks contain isolated AMR or
antibiotic-related items, but they do not provide a dedicated benchmark for AMR
agent reasoning. The gap is not a lack of AMR data. Public resources such as
BV-BRC/PATRIC, CARD/RGI, AMRFinderPlus, ResFinder, MEGARes, CRyPTIC, PLSDB, and
AMPSphere are extensive. The gap is a task design and evaluation gap: there is
no small, reproducible benchmark that asks whether agents can synthesize AMR
evidence without hallucinating genes, over-resolving uncertainty, or treating
all database disagreement as error.

We introduce AMR-Bench-mini, a focused two-track pilot benchmark:

- **GenoPheno:** given isolate metadata, an antibiotic, genome assembly path, and
  visible AMR annotation evidence, predict the retrospective AST phenotype.
- **DBReconcile:** given AMRFinderPlus and ResFinder evidence for the same
  isolate and target gene family, classify the disagreement type and produce a
  calibrated reconciliation.

The current contribution is deliberately modest: a benchmark schema, generated
pilot tasks, a deterministic rule baseline, scoring utilities, and an initial
failure-analysis workflow.

## 2. Benchmark Design

### 2.1 Scope

AMR-Bench-mini evaluates retrospective evidence synthesis. It does not evaluate
patient treatment recommendations, wet-lab protocols, pathogen engineering, or
novel antibiotic design.

The current pilot focuses on *Klebsiella pneumoniae*. The schema is intended to
be species-general, but the current dataset should not be described as a general
AMR benchmark across pathogens.

### 2.2 Data

The current scaffold contains:

- 10 public *Klebsiella pneumoniae* isolates.
- 10 local FASTA assemblies.
- 322 laboratory AST records.
- AMRFinderPlus TSV outputs for all 10 isolates.
- ResFinder outputs for all 10 isolates.
- CARD snapshot files.

The generated task set contains 212 GenoPheno tasks and 150 DBReconcile tasks.

GenoPheno phenotype labels:

| Label | Count |
| --- | ---: |
| Resistant | 154 |
| Susceptible | 50 |
| Intermediate | 8 |

DBReconcile disagreement labels:

| Disagreement type | Count |
| --- | ---: |
| drug_mapping_difference | 90 |
| gene_family_vs_allele | 33 |
| point_mutation_vs_gene_presence | 22 |
| threshold_difference | 5 |

The DBReconcile labels are currently heuristic pilot labels. They are useful for
running the harness but require manual audit before publication.

### 2.3 GenoPheno

Each GenoPheno task includes:

- isolate metadata
- genome ID and assembly path
- antibiotic and antibiotic class
- relevant AMRFinderPlus and ResFinder hits
- hidden retrospective AST label
- source provenance

The target output is structured JSON with:

- phenotype prediction
- confidence
- evidence list
- rationale
- uncertainty statement

### 2.4 DBReconcile

Each DBReconcile task includes:

- isolate metadata
- target gene family
- AMRFinderPlus gene names and evidence
- ResFinder gene names and evidence
- a pilot disagreement-type label

The current disagreement taxonomy includes:

- `drug_mapping_difference`
- `gene_family_vs_allele`
- `point_mutation_vs_gene_presence`
- `threshold_difference`

The full intended taxonomy also allows database-version differences,
intrinsic/acquired resistance differences, species-scope differences,
partial/low-quality hits, true conflicts, and insufficient evidence.

## 3. Baseline

The current executable baseline is deterministic:

- For GenoPheno, predict Resistant if any visible AMR annotation matches the
  antibiotic or antibiotic class; otherwise predict Susceptible.
- For DBReconcile, classify disagreement by simple gene-name, gene-family, and
  point-mutation heuristics.

This baseline is not meant to be a strong scientific model. It verifies that the
harness works and establishes a transparent reference point for future LLM-agent
baselines.

## 4. Pilot Results

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 362 | 1.0000 | 0.8508 | 3.7624 |
| DBReconcile | 150 | 1.0000 | 1.0000 | 2.0667 |
| GenoPheno | 212 | 1.0000 | 0.7453 | 4.9623 |

The GenoPheno result is a useful initial baseline. The DBReconcile result should
not be over-interpreted because the current gold labels are generated by related
heuristics. The next step is manual audit of DBReconcile examples and addition
of at least one LLM baseline that does not have access to the heuristic label
generation code.

## 5. Expected Failure Modes

The benchmark is designed to expose AMR-specific agent failures:

- hallucinated resistance genes
- unsupported phenotype rationales
- wrong antibiotic-class mapping
- treating database disagreement as a single-source-of-truth problem
- confusing gene-family and allele-level calls
- ignoring point-mutation versus acquired-gene scope
- ignoring tool and database versions
- overconfident answers where evidence is insufficient
- clinical-treatment language in a retrospective benchmark

## 6. Safety Statement

AMR-Bench-mini is not a clinical decision-support benchmark. It should not be
used to recommend antibiotics for patients. It excludes wet-lab protocols,
pathogen engineering, resistance optimization, and deployable antibiotic design.
Outputs that provide treatment advice or actionable wet-lab guidance should be
scored as failures.

## 7. Limitations

The current pilot has important limitations:

1. It uses only 10 isolates.
2. It focuses only on *Klebsiella pneumoniae*.
3. AST labels are retrospective and depend on source testing standards.
4. AMRFinderPlus command provenance is not fully pinned in the local artifact.
5. DBReconcile labels are heuristic and need manual audit.
6. No LLM-agent baseline has been run yet.
7. The task JSONL currently includes gold labels; a public held-out split should
   separate prompt files from answer files.

These are manageable limitations for a workshop pilot if stated clearly.

## 8. Immediate Next Steps

1. Manually audit at least 30 DBReconcile and GenoPheno outputs.
2. Split task prompts from answer keys.
3. Add an LLM baseline using the generic prompt.
4. Add an AMR-scaffolded LLM baseline using the evidence-matrix prompt.
5. Replace heuristic DBReconcile labels where manual review disagrees.
6. Add a compact figure showing the benchmark pipeline.
7. Convert this draft into the final GenBio format.

## 9. Artifact Pointers

- Benchmark README: `amr-bench/README.md`
- Task builder: `amr-bench/scripts/build_tasks.py`
- Baseline runner: `amr-bench/scripts/run_baselines.py`
- GenoPheno tasks: `amr-bench/data/tasks/genopheno.jsonl`
- DBReconcile tasks: `amr-bench/data/tasks/dbreconcile.jsonl`
- Dataset summary: `amr-bench/outputs/dataset_summary.json`
- Rule baseline summary: `amr-bench/results/rule_baseline_summary.md`
- Manual audit queue: `amr-bench/results/manual_audit.tsv`
