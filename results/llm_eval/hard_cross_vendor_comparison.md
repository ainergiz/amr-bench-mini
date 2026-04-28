# Hard MechReason Split — Cross-Vendor Comparison

**Date:** 2026-04-26  
**Split:** `data/tasks/mechreason_hard.jsonl`  
**N:** 50 hard tasks

## Headline

| Model | Provider | Composite accuracy | Mechanism-class correct | Parse-valid JSON |
|---|---|---:|---:|---:|
| `gpt-5.4` | OpenAI | 44% (22/50) | 44% (22/50) | 100% |
| `gemini-3.1-pro-preview` | Google | **58% (29/50)** | **58% (29/50)** | 100% |
| `claude-opus-4-7` | Anthropic batch | 54% (27/50) | 56% (28/50) | 100% |

The hard split successfully lowers scores versus the balanced pilot while preserving clean structural validity. The drop is concentrated in epistemic abstention and ontology cases, not in ordinary direct mechanism cases.

## Category Accuracy

| Category | n | GPT-5.4 | Gemini 3.1 Pro | Claude Opus 4.7 |
|---|---:|---:|---:|---:|
| `cefoxitin_substrate_decoy` | 10 | 4/10 | **10/10** | **10/10** |
| `cefoxitin_true_hydrolysis_control` | 3 | 3/3 | 3/3 | 3/3 |
| `drug_specificity_positive_control` | 4 | 4/4 | 4/4 | 4/4 |
| `hybrid_porin_beta_lactamase` | 4 | 4/4 | 4/4 | 3/4 |
| `hypothesisgen_insufficient_evidence` | 24 | 5/24 | 6/24 | 6/24 |
| `intrinsic_acquired_ontology` | 3 | 0/3 | 0/3 | 0/3 |
| `regulator_lof_vs_direct_efflux` | 2 | 2/2 | 2/2 | 1/2 |

## Mechanism-Class Accuracy

| Mechanism class | n | GPT-5.4 | Gemini 3.1 Pro | Claude Opus 4.7 |
|---|---:|---:|---:|---:|
| `efflux` | 4 | 4/4 | 4/4 | 4/4 |
| `enzymatic_inactivation` | 3 | 3/3 | 3/3 | 3/3 |
| `insufficient_evidence` | 24 | 5/24 | 6/24 | 6/24 |
| `intrinsic` | 3 | 0/3 | 0/3 | 0/3 |
| `permeability_loss` | 14 | 8/14 | 14/14 | 13/14 composite, 14/14 mechanism-class |
| `regulator_loss_of_function` | 2 | 2/2 | 2/2 | 1/2 |

## Failure Overlap

**Tri-vendor shared failures:** 20/50 tasks.

These consist of:

- 17 `hypothesisgen_insufficient_evidence` cases
- 3 `intrinsic_acquired_ontology` fosA cases

This is the core hard-split finding: all three vendors continue to solve clean positive controls, but most cases where the correct behavior is to recognize insufficient visible evidence remain unsolved.

## Vendor-Specific Patterns

**GPT-5.4-specific failures:** 7 tasks.

- 6 `cefoxitin_substrate_decoy` failures
- 1 additional `hypothesisgen_insufficient_evidence` failure

GPT remains weaker on cefoxitin substrate specificity: it often assigns visible non-AmpC/non-carbapenemase beta-lactamases as the primary mechanism when the gold labels porin-mediated permeability loss.

**Gemini-specific failures:** 0 tasks.

Gemini is the strongest model on this split under the current scorer: it preserves perfect cefoxitin decoy performance and still fails primarily on the shared epistemic/ontology cases.

**Claude-specific failures:** 3 tasks.

- 1 `hypothesisgen_insufficient_evidence` failure
- 1 `regulator_lof_vs_direct_efflux` failure
- 1 `hybrid_porin_beta_lactamase` composite failure

For `mechreason_kp_000713`, Claude predicted `permeability_loss`, so the mechanism class was correct, but the composite score failed due to the required-gene evidence subscore.

## Token Usage

| Model | Input tokens | Output tokens | Other reported tokens |
|---|---:|---:|---:|
| GPT-5.4 | 76,845 | 66,044 | reasoning: 0 |
| Gemini 3.1 Pro | 87,831 | 33,648 | reasoning: 74,050 |
| Claude Opus 4.7 batch | 119,380 | 76,261 | cache read/create: 0 |

Claude batch estimated cost: **$1.25**. The local OpenAI/Gemini runners record provider usage but do not yet attach provider-specific cost estimates in `summary.json`.

