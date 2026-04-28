# LLM eval summary — hard_tool_gemini-3.1-pro-preview_20260426T112234Z

- Provider/model: `gemini` / `gemini-3.1-pro-preview`
- N tasks: 50
- Timestamp: 2026-04-26T11:38:26.872299+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 50 | 1.0000 | 0.6400 | 2.5800 |
| mechreason | 50 | 1.0000 | 0.6400 | 2.5800 |

## Token usage and cost

- Input tokens: 109583
- Output tokens: 32860
- Note: No price table entry for this model. Set AMR_BENCH_PRICING_OVERRIDES to a JSON file with the same shape as PRICE_TABLE to attach a price.

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| efflux | 4 | 3 | 0.7500 |
| enzymatic_inactivation | 6 | 6 | 1.0000 |
| insufficient_evidence | 24 | 7 | 0.2917 |
| permeability_loss | 14 | 14 | 1.0000 |
| regulator_loss_of_function | 2 | 2 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.6400 |
| gene_family_correct | 0.5200 |
| layers_complete | 1.0000 |

Parse/call errors: 0