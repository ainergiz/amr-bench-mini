# LLM eval summary — smoke_20260425T192937Z

- Provider/model: `openai` / `gpt-5.4`
- N tasks: 3
- Timestamp: 2026-04-25T19:30:32.743591+00:00
- Mode: smoke (real API)

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 3 | 1.0000 | 1.0000 | 4.0000 |
| mechreason | 3 | 1.0000 | 1.0000 | 4.0000 |

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