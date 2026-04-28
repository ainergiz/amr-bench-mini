# LLM eval summary — smoke_20260425T223600Z

- Provider/model: `gemini` / `gemini-3.1-pro-preview`
- N tasks: 3
- Timestamp: 2026-04-25T22:36:59.097271+00:00
- Mode: smoke (real API)

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 3 | 1.0000 | 1.0000 | 2.6667 |
| mechreason | 3 | 1.0000 | 1.0000 | 2.6667 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| insufficient_evidence | 1 | 1 | 1.0000 |
| permeability_loss | 1 | 1 | 1.0000 |
| target_modification | 1 | 1 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 1.0000 |
| gene_family_correct | 0.6667 |
| layers_complete | 1.0000 |

Parse/call errors: 0