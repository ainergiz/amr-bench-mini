# LLM eval summary — hard_gemini-3.1-pro-preview_20260426Tmanual

- Provider/model: `gemini` / `gemini-3.1-pro-preview`
- N tasks: 50
- Timestamp: 2026-04-26T10:19:19.772886+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 50 | 1.0000 | 0.5800 | 2.5200 |
| mechreason | 50 | 1.0000 | 0.5800 | 2.5200 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| efflux | 4 | 4 | 1.0000 |
| enzymatic_inactivation | 3 | 3 | 1.0000 |
| insufficient_evidence | 24 | 6 | 0.2500 |
| intrinsic | 3 | 0 | 0.0000 |
| permeability_loss | 14 | 14 | 1.0000 |
| regulator_loss_of_function | 2 | 2 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.5800 |
| gene_family_correct | 0.5200 |
| layers_complete | 1.0000 |

Parse/call errors: 0