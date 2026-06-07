# MechReason Label Audit Summary

This file summarizes the adjudication loop used to harden MechReason mechanism
labels after the initial deterministic heuristic pass.

## Overview

| Quantity | Value |
|---|---:|
| Cards reviewed across two rounds | 60 |
| Round 1 sample | 31 |
| Round 2 sample | 29 |
| Systematic heuristic-priority errors corrected | 5 |
| Round 1 non-KEEP rate | 29.0% |
| Round 2 non-KEEP rate | 6.9% |

The audit was used to identify systematic label-priority errors, patch the
heuristic, and retain ambiguous co-mechanism cases with explicit secondary
mechanism metadata where appropriate.

## Round 1: Pre-Fix Audit

| Decision | Count | Fraction |
|---|---:|---:|
| KEEP | 22 | 71.0% |
| OVERRIDE | 5 | 16.1% |
| AMBIGUOUS | 4 | 12.9% |

The first pass surfaced three priority errors:

1. Tetracycline tasks with direct tet(A) evidence were over-called as
   `regulator_loss_of_function` when a drug-specific efflux call was the
   dominant visible mechanism.
2. Cefoxitin resistance with non-AmpC beta-lactamases plus OmpK porin lesions
   was over-called as `enzymatic_inactivation`; cefoxitin resistance was driven
   by permeability loss unless an AmpC or carbapenemase mechanism was visible.
3. Tigecycline resistance with wild-type tet(A)/oqxAB but no regulator
   loss-of-function evidence was over-called as `efflux`; these cases should
   remain `insufficient_evidence`.

## Round 2: Post-Fix Audit

After patching the first three priority errors in
`scripts/build_tasks.py::infer_mechanism()` and rebuilding the corpus, a fresh
stratified sample of 29 cards was reviewed.

| Decision | Count | Fraction |
|---|---:|---:|
| KEEP | 27 | 93.1% |
| OVERRIDE | 1 | 3.4% |
| AMBIGUOUS | 1 | 3.4% |

The second pass surfaced two additional issues:

4. Cefoxitin resistance with KPC carbapenemase evidence should be labeled
   `enzymatic_inactivation`, because KPC-family carbapenemases can hydrolyze
   cefoxitin.
5. Beta-lactamase family detection used substring matching, allowing `act` to
   match inside normalized `blaCTX-M` gene names. The fix strips a leading
   `bla` prefix and applies prefix matching to the remaining family name.

## Current Mechanism Distribution

| Class | Pre-fix Round 1 | After fixes 1-3 | Current |
|---|---:|---:|---:|
| `enzymatic_inactivation` | 332 | 685 | 670 |
| `permeability_loss` | 373 | 33 | 35 |
| `insufficient_evidence` | 15 | 24 | 24 |
| `regulator_loss_of_function` | 14 | 2 | 2 |
| `target_modification` | 84 | 92 | 92 |
| `efflux` | 52 | 47 | 47 |
| `metabolic_bypass` | 51 | 51 | 51 |
| `intrinsic` | 3 | 3 | 3 |

## Hybrid Mechanisms

Ambiguous cases with genuine co-driving mechanisms are represented by optional
gold fields:

```json
{
  "gold": {
    "mechanism_class": "permeability_loss",
    "secondary_mechanism_classes": ["enzymatic_inactivation"],
    "interaction_type": "synergistic",
    "required_genes": ["ompk35e42rfster47"]
  }
}
```

`secondary_mechanism_classes` and `interaction_type` are optional and are absent
for ordinary single-mechanism cases. Existing scoring ignores these fields
unless a downstream analysis explicitly uses them.
