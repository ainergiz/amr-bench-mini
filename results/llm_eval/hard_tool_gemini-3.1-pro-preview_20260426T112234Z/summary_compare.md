# Strict vs adjusted rescoring — hard_tool_gemini-3.1-pro-preview_20260426T112234Z

Original `summary.json` is untouched. The strict score uses the pre-adjudication gold (`data/tasks/mechreason_strict.jsonl`); the adjusted score uses the audit-adjudicated gold (`data/tasks/mechreason.jsonl`).

| Metric | Strict | Adjusted |
| --- | ---: | ---: |
| Composite accuracy | 0.5800 (29/50) | 0.6400 (32/50) |
| JSON valid rate | 1.0000 | 1.0000 |
| Mean evidence items | 2.5800 | 2.5800 |

## MechReason — per-class composite accuracy

| Class | n strict | strict acc | n adjusted | adjusted acc |
| --- | ---: | ---: | ---: | ---: |
| `efflux` | 4 | 0.7500 | 4 | 0.7500 |
| `enzymatic_inactivation` | 3 | 1.0000 | 6 | 1.0000 |
| `insufficient_evidence` | 24 | 0.2917 | 24 | 0.2917 |
| `intrinsic` | 3 | 0.0000 | 0 | 0.0000 |
| `permeability_loss` | 14 | 1.0000 | 14 | 1.0000 |
| `regulator_loss_of_function` | 2 | 1.0000 | 2 | 1.0000 |

## Score flips (3)

| task_id | strict_gold | adjusted_gold | prediction | strict | adjusted |
| --- | --- | --- | --- | :-: | :-: |
| mechreason_kp_000357 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
| mechreason_kp_000866 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
| mechreason_kp_000896 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
