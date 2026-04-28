# LLM eval summary — pilot_batch_claude-opus-4-7_20260426T083024Z

- Provider/model: `anthropic_batch` / `claude-opus-4-7`
- N tasks: 50
- Timestamp: 2026-04-26T08:31:56.686810+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 50 | 1.0000 | 0.7800 | 4.4800 |
| mechreason | 50 | 1.0000 | 0.7800 | 4.4800 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| efflux | 6 | 6 | 1.0000 |
| enzymatic_inactivation | 10 | 9 | 0.9000 |
| insufficient_evidence | 8 | 2 | 0.2500 |
| intrinsic | 3 | 0 | 0.0000 |
| metabolic_bypass | 4 | 4 | 1.0000 |
| permeability_loss | 10 | 10 | 1.0000 |
| regulator_loss_of_function | 2 | 1 | 0.5000 |
| target_modification | 7 | 7 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.7800 |
| gene_family_correct | 0.8400 |
| layers_complete | 1.0000 |

Parse/call errors: 0

## Anthropic batch cost estimate

- Batch ID: `msgbatch_01YUfcYkGVHwbMEJ5zYFBTG3`
- Elapsed: 91.958s
- Input tokens: 131206
- Output tokens: 79243
- List-price cost: $2.6371
- Batch estimated cost: **$1.3186**
