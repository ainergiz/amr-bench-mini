# Strict vs adjusted rescoring — two_task_hard_claude-opus-4-7_20260426Tmanual

Original `summary.json` is untouched. The strict score uses the pre-adjudication gold (`data/tasks/mechreason_strict.jsonl`); the adjusted score uses the audit-adjudicated gold (`data/tasks/mechreason.jsonl`).

| Metric | Strict | Adjusted |
| --- | ---: | ---: |
| Composite accuracy | 0.5000 (1/2) | 0.5000 (1/2) |
| JSON valid rate | 1.0000 | 1.0000 |
| Mean evidence items | 4.5000 | 4.5000 |

## MechReason — per-class composite accuracy

| Class | n strict | strict acc | n adjusted | adjusted acc |
| --- | ---: | ---: | ---: | ---: |
| `insufficient_evidence` | 1 | 0.0000 | 1 | 0.0000 |
| `permeability_loss` | 1 | 1.0000 | 1 | 1.0000 |

## Score flips (0)

*No flips between strict and adjusted scoring.*
