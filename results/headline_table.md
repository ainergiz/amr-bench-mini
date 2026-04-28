# Headline Table — Strict and Audit-Adjudicated Accuracy

All accuracies report Wilson 95% CIs when subgroup *n* ≥ 10. Rare subgroups (*n* < 10) report point estimates only and are not used for population claims.

Strict gold = pre-adjudication heuristic labels (`data/tasks/mechreason_strict.jsonl`).  
Adjudicated gold = post-audit labels with the four invariant overrides (3× *fosA* `intrinsic` → `enzymatic_inactivation`; 1× ArmA hybrid `enzymatic_inactivation` → `target_modification` + secondary `enzymatic_inactivation`) (`data/tasks/mechreason.jsonl`).

## Overall composite accuracy

| Split | Model | Strict accuracy | Adjudicated accuracy |
| --- | --- | --- | --- |
| Balanced pilot (n=50) | GPT-5.4 | 74.0% [60.4%, 84.1%] (37/50) | 82.0% [69.2%, 90.2%] (41/50) |
| Balanced pilot (n=50) | Gemini 3.1 Pro | 80.0% [67.0%, 88.8%] (40/50) | 88.0% [76.2%, 94.4%] (44/50) |
| Balanced pilot (n=50) | Claude Opus 4.7 | 78.0% [64.8%, 87.2%] (39/50) | 86.0% [73.8%, 93.0%] (43/50) |
| Hard diagnostic (n=50) | GPT-5.4 | 44.0% [31.2%, 57.7%] (22/50) | 50.0% [36.6%, 63.4%] (25/50) |
| Hard diagnostic (n=50) | Gemini 3.1 Pro | 58.0% [44.2%, 70.6%] (29/50) | 64.0% [50.1%, 75.9%] (32/50) |
| Hard diagnostic (n=50) | Claude Opus 4.7 | 54.0% [40.4%, 67.0%] (27/50) | 60.0% [46.2%, 72.4%] (30/50) |

## Hard split — per-category accuracy (adjudicated gold)

Per-category Wilson CIs are reported for `hypothesisgen_insufficient_evidence` and `cefoxitin_substrate_decoy` only (n ≥ 10). The other five categories provide contrastive controls and ontology stress tests; their accuracies are reported as point estimates and are not used for population claims.

| Category | n | GPT-5.4 | Gemini 3.1 Pro | Claude Opus 4.7 |
| --- | ---: | --- | --- | --- |
| `hypothesisgen_insufficient_evidence` | 24 | 20.8% [9.2%, 40.5%] (5/24) | 25.0% [12.0%, 44.9%] (6/24) | 25.0% [12.0%, 44.9%] (6/24) |
| `cefoxitin_substrate_decoy` | 10 | 40.0% [16.8%, 68.7%] (4/10) | 100.0% [72.2%, 100.0%] (10/10) | 100.0% [72.2%, 100.0%] (10/10) |
| `drug_specificity_positive_control` | 4 | 100.0% (4/4) | 100.0% (4/4) | 100.0% (4/4) |
| `hybrid_porin_beta_lactamase` | 4 | 100.0% (4/4) | 100.0% (4/4) | 75.0% (3/4) |
| `cefoxitin_true_hydrolysis_control` | 3 | 100.0% (3/3) | 100.0% (3/3) | 100.0% (3/3) |
| `intrinsic_acquired_ontology` | 3 | 100.0% (3/3) | 100.0% (3/3) | 100.0% (3/3) |
| `regulator_lof_vs_direct_efflux` | 2 | 100.0% (2/2) | 100.0% (2/2) | 50.0% (1/2) |

## Pilot split — per-class accuracy (adjudicated gold)

Per-class CIs are reported only where pilot subgroup n ≥ 10.

| Class | n | GPT-5.4 | Gemini 3.1 Pro | Claude Opus 4.7 |
| --- | ---: | --- | --- | --- |
| `enzymatic_inactivation` | 12 | 100.0% [75.8%, 100.0%] (12/12) | 100.0% [75.8%, 100.0%] (12/12) | 100.0% [75.8%, 100.0%] (12/12) |
| `permeability_loss` | 10 | 80.0% [49.0%, 94.3%] (8/10) | 100.0% [72.2%, 100.0%] (10/10) | 100.0% [72.2%, 100.0%] (10/10) |
| `target_modification` | 8 | 100.0% (8/8) | 100.0% (8/8) | 100.0% (8/8) |
| `insufficient_evidence` | 8 | 25.0% (2/8) | 25.0% (2/8) | 25.0% (2/8) |
| `efflux` | 6 | 100.0% (6/6) | 100.0% (6/6) | 100.0% (6/6) |
| `metabolic_bypass` | 4 | 75.0% (3/4) | 100.0% (4/4) | 100.0% (4/4) |
| `regulator_loss_of_function` | 2 | 100.0% (2/2) | 100.0% (2/2) | 50.0% (1/2) |

## Rare-class strategy

We report Wilson 95% CIs only when subgroup *n* ≥ 10. Below this threshold, point estimates are reported descriptively without intervals to avoid implying population precision that the data do not support. Rare-class members in this benchmark are:

- `intrinsic` (n=3 in pilot, 3 in hard) — three *fosA* tasks; reported under `intrinsic_acquired_ontology` to expose the strict-vs-adjudicated gap.
- `regulator_loss_of_function` (n=2 in pilot, 2 in hard) — diagnostic controls for regulator-vs-direct-efflux causality.
- `cefoxitin_true_hydrolysis_control` (n=3 hard only), `drug_specificity_positive_control` (n=4 hard only), `hybrid_porin_beta_lactamase` (n=4 hard only) — contrastive controls; all three are passed by all three models in the current adjudicated runs.

We do **not** collapse rare classes into a generic `rare-mechanism` bucket because the categories are diagnostic of distinct reasoning failures (ontology vs. causality vs. hybrid mechanisms). Pooling would obscure the exact failure mode the split was constructed to expose.
