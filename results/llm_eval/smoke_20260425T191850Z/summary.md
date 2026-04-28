# LLM eval summary — smoke_20260425T191850Z

- Provider/model: `mock` / `smoke-mock-v1`
- N tasks: 3
- Timestamp: 2026-04-25T19:18:50.779434+00:00
- Mode: smoke (mocked model)

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 3 | 1.0000 | 0.0000 | 1.0000 |
| mechreason | 3 | 1.0000 | 0.0000 | 1.0000 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| insufficient_evidence | 1 | 0 | 0.0000 |
| permeability_loss | 1 | 0 | 0.0000 |
| target_modification | 1 | 0 | 0.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.0000 |
| gene_family_correct | 0.0000 |
| layers_complete | 1.0000 |

Parse/call errors: 0