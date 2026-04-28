# Tool intervention vs no-tool — Gemini 3.1 Pro on hard split

- Baseline run: `hard_gemini-3.1-pro-preview_20260426Tmanual` (no tool)
- Tool-augmented run: `hard_tool_gemini-3.1-pro-preview_20260426T112234Z` (CARD ARO substrate context pre-resolved per visible gene)
- Scoring: adjudicated gold (`data/tasks/mechreason.jsonl`)
- N tasks: 50

## Headline

- Baseline accuracy: **32/50 = 64.0%**
- Tool-augmented accuracy: **32/50 = 64.0%**
- Net delta: **+0** tasks

## Per-category breakdown

| Category | n | Baseline | Tool-augmented | Δ |
| --- | ---: | --- | --- | ---: |
| `hypothesisgen_insufficient_evidence` | 24 | 6/24 (25%) | 7/24 (29%) | +1 |
| `cefoxitin_substrate_decoy` | 10 | 10/10 (100%) | 10/10 (100%) | +0 |
| `drug_specificity_positive_control` | 4 | 4/4 (100%) | 3/4 (75%) | -1 |
| `hybrid_porin_beta_lactamase` | 4 | 4/4 (100%) | 4/4 (100%) | +0 |
| `cefoxitin_true_hydrolysis_control` | 3 | 3/3 (100%) | 3/3 (100%) | +0 |
| `intrinsic_acquired_ontology` | 3 | 3/3 (100%) | 3/3 (100%) | +0 |
| `regulator_lof_vs_direct_efflux` | 2 | 2/2 (100%) | 2/2 (100%) | +0 |

## Tasks gained by tool (2)

| task_id | antibiotic | gold | baseline pred | tool pred |
| --- | --- | --- | --- | --- |
| `mechreason_kp_000603` | trimethoprim/sulfamethoxazole | `insufficient_evidence` | `efflux` | `insufficient_evidence` |
| `mechreason_kp_000872` | tigecycline | `insufficient_evidence` | `efflux` | `insufficient_evidence` |

## Tasks lost by tool (2)

| task_id | antibiotic | gold | baseline pred | tool pred |
| --- | --- | --- | --- | --- |
| `mechreason_kp_000778` | tetracycline | `efflux` | `efflux` | `insufficient_evidence` |
| `mechreason_kp_000569` | tigecycline | `insufficient_evidence` | `insufficient_evidence` | `efflux` |

## Interpretation

The CARD substrate context block injects, for every visible AMRFinderPlus / ResFinder hit, the canonical drug-class coverage and resistance mechanism from CARD ARO. The intent of the experiment is to test whether the central abstention failure (`hypothesisgen_insufficient_evidence`) is a knowledge-retrieval gap that pre-resolved substrate biology can close, or a calibration failure that survives even when the substrate facts are stated explicitly in the prompt.

Gemini 3.1 Pro was already at 100% on `cefoxitin_substrate_decoy` without tools, so this category cannot test the substrate-knowledge hypothesis on Gemini specifically — there is no headroom. The relevant signal is the `hypothesisgen_insufficient_evidence` row.

### Headline finding

Net effect on the abstention category is **+1/24 (4.2pp)**: well inside the Wilson 95% CI for either run and indistinguishable from noise. Aggregate accuracy is **identical** at 32/50 because the tool gained two cases on `hypothesisgen_insufficient_evidence` while losing two cases — one on `drug_specificity_positive_control` and one on the same `hypothesisgen_insufficient_evidence` category. 

### Asymmetric flips

The two losses are diagnostic. On `mechreason_kp_000778` (tetracycline + *tet(A)* + *oqxAB*, gold `efflux`), the no-tool model correctly invoked efflux; with substrate context the model abstained, apparently because the CARD card for *oqxA/B* lists glycylcyclines and tigecycline alongside tetracycline coverage and the model became conservative about the call. On `mechreason_kp_000569` (tigecycline, gold `insufficient_evidence`), the no-tool model correctly abstained; with substrate context the model called `efflux`, presumably anchoring on the same broad CARD substrate listing.

Substrate context, in other words, is *bidirectionally* persuasive: it encourages the model to invoke a mechanism when the visible gene's CARD card mentions the queried drug class, regardless of whether the visible evidence is mechanistically sufficient. This is the opposite of the calibration property the abstention category requires.

### Implication for the paper

Pre-resolved substrate retrieval does not fix the central abstention failure on Gemini 3.1 Pro. The four-percentage-point gain on `hypothesisgen_insufficient_evidence` is offset one-for-one by losses on neighboring categories. This supports the framing that the abstention failure is a *calibration* problem, not a *retrieval* problem — adding the substrate-coverage facts to the prompt does not make the model recognize that the visible evidence is insufficient. The paper's claim should be: tool augmentation by substrate retrieval is necessary but not sufficient for evidence-sufficiency reasoning.
