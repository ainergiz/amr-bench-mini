# LLM eval summary — two_task_hard_claude-opus-4-7_20260426Tmanual

- Provider/model: `anthropic` / `claude-opus-4-7`
- N tasks: 2
- Timestamp: 2026-04-26T08:15:15.746839+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 2 | 1.0000 | 0.5000 | 4.5000 |
| mechreason | 2 | 1.0000 | 0.5000 | 4.5000 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| insufficient_evidence | 1 | 0 | 0.0000 |
| permeability_loss | 1 | 1 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.5000 |
| gene_family_correct | 0.5000 |
| layers_complete | 1.0000 |

Parse/call errors: 0