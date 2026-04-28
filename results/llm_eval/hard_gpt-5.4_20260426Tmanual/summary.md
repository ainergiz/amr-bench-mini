# LLM eval summary — hard_gpt-5.4_20260426Tmanual

- Provider/model: `openai` / `gpt-5.4`
- N tasks: 50
- Timestamp: 2026-04-26T10:20:50.481271+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 50 | 1.0000 | 0.4400 | 4.4600 |
| mechreason | 50 | 1.0000 | 0.4400 | 4.4600 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| efflux | 4 | 4 | 1.0000 |
| enzymatic_inactivation | 3 | 3 | 1.0000 |
| insufficient_evidence | 24 | 5 | 0.2083 |
| intrinsic | 3 | 0 | 0.0000 |
| permeability_loss | 14 | 8 | 0.5714 |
| regulator_loss_of_function | 2 | 2 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.4400 |
| gene_family_correct | 0.5200 |
| layers_complete | 1.0000 |

Parse/call errors: 0