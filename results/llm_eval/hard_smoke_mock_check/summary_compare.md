# Strict vs adjusted rescoring — hard_smoke_mock_check

Original `summary.json` is untouched. The strict score uses the pre-adjudication gold (`data/tasks/mechreason_strict.jsonl`); the adjusted score uses the audit-adjudicated gold (`data/tasks/mechreason.jsonl`).

| Metric | Strict | Adjusted |
| --- | ---: | ---: |
| Composite accuracy | 0.0000 (0/3) | 0.0000 (0/3) |
| JSON valid rate | 1.0000 | 1.0000 |
| Mean evidence items | 1.0000 | 1.0000 |

## MechReason — per-class composite accuracy

| Class | n strict | strict acc | n adjusted | adjusted acc |
| --- | ---: | ---: | ---: | ---: |
| `permeability_loss` | 3 | 0.0000 | 3 | 0.0000 |

## Score flips (0)

*No flips between strict and adjusted scoring.*
