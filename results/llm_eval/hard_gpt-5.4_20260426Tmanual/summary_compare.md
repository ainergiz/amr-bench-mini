# Strict vs adjusted rescoring — hard_gpt-5.4_20260426Tmanual

Original `summary.json` is untouched. The strict score uses the pre-adjudication gold (`data/tasks/mechreason_strict.jsonl`); the adjusted score uses the audit-adjudicated gold (`data/tasks/mechreason.jsonl`).

| Metric | Strict | Adjusted |
| --- | ---: | ---: |
| Composite accuracy | 0.4400 (22/50) | 0.5000 (25/50) |
| JSON valid rate | 1.0000 | 1.0000 |
| Mean evidence items | 4.4600 | 4.4600 |

## MechReason — per-class composite accuracy

| Class | n strict | strict acc | n adjusted | adjusted acc |
| --- | ---: | ---: | ---: | ---: |
| `efflux` | 4 | 1.0000 | 4 | 1.0000 |
| `enzymatic_inactivation` | 3 | 1.0000 | 6 | 1.0000 |
| `insufficient_evidence` | 24 | 0.2083 | 24 | 0.2083 |
| `intrinsic` | 3 | 0.0000 | 0 | 0.0000 |
| `permeability_loss` | 14 | 0.5714 | 14 | 0.5714 |
| `regulator_loss_of_function` | 2 | 1.0000 | 2 | 1.0000 |

## Score flips (3)

| task_id | strict_gold | adjusted_gold | prediction | strict | adjusted |
| --- | --- | --- | --- | :-: | :-: |
| mechreason_kp_000357 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
| mechreason_kp_000866 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
| mechreason_kp_000896 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
