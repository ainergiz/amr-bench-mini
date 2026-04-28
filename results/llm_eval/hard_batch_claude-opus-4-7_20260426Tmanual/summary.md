# LLM eval summary — hard_batch_claude-opus-4-7_20260426Tmanual

- Provider/model: `anthropic_batch` / `claude-opus-4-7`
- N tasks: 50
- Timestamp: 2026-04-26T09:59:38.035970+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 50 | 1.0000 | 0.5400 | 3.8800 |
| mechreason | 50 | 1.0000 | 0.5400 | 3.8800 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| efflux | 4 | 4 | 1.0000 |
| enzymatic_inactivation | 3 | 3 | 1.0000 |
| insufficient_evidence | 24 | 6 | 0.2500 |
| intrinsic | 3 | 0 | 0.0000 |
| permeability_loss | 14 | 13 | 0.9286 |
| regulator_loss_of_function | 2 | 1 | 0.5000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.5600 |
| gene_family_correct | 0.5000 |
| layers_complete | 1.0000 |

Parse/call errors: 0

## Anthropic batch cost estimate

- Batch ID: `msgbatch_01JCt78HzbuXvyB54xzRH3kq`
- Elapsed: 121.892s
- Input tokens: 119380
- Output tokens: 76261
- List-price cost: $2.5034
- Batch estimated cost: **$1.2517**
