# LLM eval summary — gemini_batch_smoke_20260426T114739Z

- Provider/model: `gemini_batch` / `gemini-3.1-pro-preview`
- N tasks: 5
- Timestamp: 2026-04-26T12:06:50.748237+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 5 | 1.0000 | 1.0000 | 3.0000 |
| mechreason | 5 | 1.0000 | 1.0000 | 3.0000 |

## Token usage and cost

- Input tokens: 9862
- Output tokens: 3938
- Note: No price table entry for this model. Set AMR_BENCH_PRICING_OVERRIDES to a JSON file with the same shape as PRICE_TABLE to attach a price.

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| permeability_loss | 5 | 5 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 1.0000 |
| gene_family_correct | 1.0000 |
| layers_complete | 1.0000 |

Parse/call errors: 0

## Gemini batch metadata

- Batch ID: `batches/7jw5w6dgflemgw8ieg7fr4augmk1051u0mvb`
- Elapsed: 1150.8s
- Input tokens: 9862
- Output tokens: 3938
- Note: No price table entry for this model. Set AMR_BENCH_PRICING_OVERRIDES to a JSON file with the same shape as PRICE_TABLE to attach a price.
