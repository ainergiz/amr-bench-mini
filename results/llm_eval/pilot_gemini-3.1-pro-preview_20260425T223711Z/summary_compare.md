# Strict vs adjusted rescoring — pilot_gemini-3.1-pro-preview_20260425T223711Z

Original `summary.json` is untouched. The strict score uses the pre-adjudication gold (`data/tasks/mechreason_strict.jsonl`); the adjusted score uses the audit-adjudicated gold (`data/tasks/mechreason.jsonl`).

| Metric | Strict | Adjusted |
| --- | ---: | ---: |
| Composite accuracy | 0.8000 (40/50) | 0.8800 (44/50) |
| JSON valid rate | 1.0000 | 1.0000 |
| Mean evidence items | 2.9200 | 2.9200 |

## MechReason — per-class composite accuracy

| Class | n strict | strict acc | n adjusted | adjusted acc |
| --- | ---: | ---: | ---: | ---: |
| `efflux` | 6 | 1.0000 | 6 | 1.0000 |
| `enzymatic_inactivation` | 10 | 0.9000 | 12 | 1.0000 |
| `insufficient_evidence` | 8 | 0.2500 | 8 | 0.2500 |
| `intrinsic` | 3 | 0.0000 | 0 | 0.0000 |
| `metabolic_bypass` | 4 | 1.0000 | 4 | 1.0000 |
| `permeability_loss` | 10 | 1.0000 | 10 | 1.0000 |
| `regulator_loss_of_function` | 2 | 1.0000 | 2 | 1.0000 |
| `target_modification` | 7 | 1.0000 | 8 | 1.0000 |

## Score flips (4)

| task_id | strict_gold | adjusted_gold | prediction | strict | adjusted |
| --- | --- | --- | --- | :-: | :-: |
| mechreason_kp_000830 | `enzymatic_inactivation` | `target_modification` | `target_modification` | ✗ | ✓ |
| mechreason_kp_000357 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
| mechreason_kp_000866 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
| mechreason_kp_000896 | `intrinsic` | `enzymatic_inactivation` | `enzymatic_inactivation` | ✗ | ✓ |
