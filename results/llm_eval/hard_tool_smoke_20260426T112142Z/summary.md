# LLM eval summary — hard_tool_smoke_20260426T112142Z

- Provider/model: `gemini` / `gemini-3.1-pro-preview`
- N tasks: 2
- Timestamp: 2026-04-26T11:22:27.531582+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 2 | 1.0000 | 1.0000 | 3.0000 |
| mechreason | 2 | 1.0000 | 1.0000 | 3.0000 |

## Token usage and cost

- Input tokens: 5206
- Output tokens: 1557
- Note: No price table entry for this model. Set AMR_BENCH_PRICING_OVERRIDES to a JSON file with the same shape as PRICE_TABLE to attach a price.

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| permeability_loss | 2 | 2 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 1.0000 |
| gene_family_correct | 1.0000 |
| layers_complete | 1.0000 |

Parse/call errors: 0