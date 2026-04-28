# LLM eval summary — pilot_gpt-5.4_20260425T193051Z

- Provider/model: `openai` / `gpt-5.4`
- N tasks: 50
- Timestamp: 2026-04-25T19:50:15.883756+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 50 | 1.0000 | 0.7400 | 5.2800 |
| mechreason | 50 | 1.0000 | 0.7400 | 5.2800 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| efflux | 6 | 6 | 1.0000 |
| enzymatic_inactivation | 10 | 9 | 0.9000 |
| insufficient_evidence | 8 | 2 | 0.2500 |
| intrinsic | 3 | 0 | 0.0000 |
| metabolic_bypass | 4 | 3 | 0.7500 |
| permeability_loss | 10 | 8 | 0.8000 |
| regulator_loss_of_function | 2 | 2 | 1.0000 |
| target_modification | 7 | 7 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.7400 |
| gene_family_correct | 0.8400 |
| layers_complete | 1.0000 |

Parse/call errors: 0