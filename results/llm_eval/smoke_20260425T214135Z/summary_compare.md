# Strict vs adjusted rescoring — smoke_20260425T214135Z

Original `summary.json` is untouched. The strict score uses the pre-adjudication gold (`data/tasks/mechreason_strict.jsonl`); the adjusted score uses the audit-adjudicated gold (`data/tasks/mechreason.jsonl`).

| Metric | Strict | Adjusted |
| --- | ---: | ---: |
| Composite accuracy | 1.0000 (3/3) | 1.0000 (3/3) |
| JSON valid rate | 1.0000 | 1.0000 |
| Mean evidence items | 4.3333 | 4.3333 |

## MechReason — per-class composite accuracy

| Class | n strict | strict acc | n adjusted | adjusted acc |
| --- | ---: | ---: | ---: | ---: |
| `insufficient_evidence` | 1 | 1.0000 | 1 | 1.0000 |
| `permeability_loss` | 1 | 1.0000 | 1 | 1.0000 |
| `target_modification` | 1 | 1.0000 | 1 | 1.0000 |

## Score flips (0)

*No flips between strict and adjusted scoring.*
