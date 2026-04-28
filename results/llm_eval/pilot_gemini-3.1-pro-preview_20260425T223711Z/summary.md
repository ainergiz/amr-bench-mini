# LLM eval summary — pilot_gemini-3.1-pro-preview_20260425T223711Z

- Provider/model: `gemini` / `gemini-3.1-pro-preview`
- N tasks: 50
- Timestamp: 2026-04-25T22:51:08.757981+00:00

| Split | n | JSON valid | Accuracy | Mean evidence items |
| --- | ---: | ---: | ---: | ---: |
| overall | 50 | 1.0000 | 0.8000 | 2.9200 |
| mechreason | 50 | 1.0000 | 0.8000 | 2.9200 |

## MechReason — per-class accuracy

| Mechanism class | n | correct | accuracy |
| --- | ---: | ---: | ---: |
| efflux | 6 | 6 | 1.0000 |
| enzymatic_inactivation | 10 | 9 | 0.9000 |
| insufficient_evidence | 8 | 2 | 0.2500 |
| intrinsic | 3 | 0 | 0.0000 |
| metabolic_bypass | 4 | 4 | 1.0000 |
| permeability_loss | 10 | 10 | 1.0000 |
| regulator_loss_of_function | 2 | 2 | 1.0000 |
| target_modification | 7 | 7 | 1.0000 |

## MechReason — subscore rates

| Subscore | rate |
| --- | ---: |
| mechanism_class_correct | 0.8000 |
| gene_family_correct | 0.8400 |
| layers_complete | 1.0000 |

Parse/call errors: 0