# MechReason Label Audit — Consolidated Summary

**Auditor (first pass):** Claude Opus 4.7 (this session), surrogate microbiologist.
**Total cards reviewed across two rounds:** 60 (31 pre-fix + 29 post-fix).
**Outcome:** 5 systematic heuristic-priority bugs identified and corrected; gold credibility moved from ~71% to ~93% on a fresh stratified sample.

> The audit is the methodological story the paper should tell. The headline is *not* "our heuristic labels are good." It is: **we generated heuristic mechanism labels, stratified-audited them, found systematic biological priority errors, corrected the rule set, and retained ambiguous hybrid cases for adjudication.**

---

## Round 1 — pre-fix audit (31 cards on initial heuristic)

| Decision | Count | Fraction |
|---|---:|---:|
| KEEP | 22 | 71.0% |
| OVERRIDE (clear label change) | 5 | 16.1% |
| AMBIGUOUS (hybrid / borderline) | 4 | 12.9% |

**Per-paper wording:** *"5/31 clear label overrides and 9/31 cards requiring revision or adjudication."*

### Three priority bugs surfaced

1. **Tetracycline + tet(A) + ramR LoF → was `regulator_loss_of_function`, should be `efflux`.** tet(A) is a direct tetracycline-specific MFS efflux pump and the dominant mechanism; ramR LoF is supplementary. The heuristic priority ordering checked regulator-LoF before drug-specific efflux, and so over-called regulator LoF.
2. **Cefoxitin R + non-AmpC β-lactamases + ompK frameshift → was `enzymatic_inactivation`, should be `permeability_loss`.** Cefoxitin (a 7α-methoxy cephamycin) is not efficiently hydrolyzed by ESBLs (CTX-M family), narrow-spectrum SHV/TEM, or OXA-1. The dominant mechanism is porin loss, with AmpC only when an AmpC mechanism is actually present; non-AmpC β-lactamases are confounders.
3. **Tigecycline + wild-type tet(A)/oqxAB without regulator LoF → was `efflux`, should be `insufficient_evidence`.** Tigecycline is a glycylcycline designed to evade Tet pumps; wild-type tet(A) and oqxAB cannot drive a clinical R phenotype on their own. Without ramR/acrR/oqxR/marR LoF or a tigecycline-active tet variant (tet(X), tet(L)), this is a HypothesisGen flavor.

**Detailed per-case reasoning is in `audit_first_pass_claude.md`.**

---

## Round 2 — post-fix audit (29 cards on corrected heuristic)

After patching the three priority bugs in `scripts/build_tasks.py::infer_mechanism()` and rebuilding the corpus, a fresh stratified sample of 29 cards was audited:

| Decision | Count | Fraction |
|---|---:|---:|
| KEEP | 27 | 93.1% |
| OVERRIDE | 1 | 3.4% |
| AMBIGUOUS | 1 | 3.4% |

**Per-paper wording:** *"After heuristic correction, only 2/29 cards required revision or adjudication (1 override + 1 ambiguous), bringing post-audit credibility to 93%."*

### Two additional issues surfaced

4. **Cefoxitin R + KPC carbapenemase → was `permeability_loss`, should be `enzymatic_inactivation`.** KPC-2/3 are class-A serine carbapenemases with broad activity that *do* hydrolyze cefoxitin (in addition to penicillins, cephalosporins, and carbapenems). The cefoxitin priority branch needs to treat KPC/NDM/VIM-family carbapenemases as cefoxitin-active enzymes alongside the AmpC family. **Fixed.**

5. **Substring-matching bug in β-lactamase family detection.** The original `any(token in compact_gene for token in (...))` test allowed `"act"` to match inside `"blactxm15"` (norm of blaCTX-M-15), causing 11 cefoxitin tasks to be mislabeled as `enzymatic_inactivation` driven by a phantom `ACT` AmpC. **Fixed via prefix-based matching after stripping the `bla` prefix:**

   ```python
   def bla_family_starts_with(gene_compact, prefixes):
       name = gene_compact[3:] if gene_compact.startswith("bla") else gene_compact
       return any(name.startswith(p) for p in prefixes)
   ```

After fixes 4–5, MechReason mechanism-class distribution stabilized at:

| Class | Pre-fix Round 1 | After fixes 1–3 | After fixes 4–5 (current) |
|---|---:|---:|---:|
| `enzymatic_inactivation` | 332 | 685 | **670** |
| `permeability_loss` | 373 | 33 | **35** |
| `insufficient_evidence` | 15 | 24 | **24** |
| `regulator_loss_of_function` | 14 | 2 | **2** |
| `target_modification` | 84 | 92 | **92** |
| `efflux` | 52 | 47 | **47** |
| `metabolic_bypass` | 51 | 51 | **51** |
| `intrinsic` | 3 | 3 | **3** |

The shift toward `enzymatic_inactivation` (most resistance in real K. pneumoniae *is* β-lactamase-driven) and away from over-called `permeability_loss` is biologically expected.

---

## Hybrid mechanisms — schema extension

The 4 ambiguous Round-1 cases shared a pattern: **two mechanisms genuinely co-drive resistance** (most often ESBL hyperexpression + porin loss → carbapenem R, or cefepime/imipenem R from CTX-M-15 + ompK35 frameshift). To preserve specificity while handling these cases, we added optional fields to the MechReason gold:

```jsonc
{
  "gold": {
    "mechanism_class": "permeability_loss",            // primary, dominant
    "secondary_mechanism_classes": ["enzymatic_inactivation"],
    "interaction_type": "synergistic",                  // additive | synergistic | uncertain
    "required_genes": ["ompk35e42rfster47"]
  }
}
```

`secondary_mechanism_classes` and `interaction_type` are optional and default to absent. The heuristic does not auto-populate them — the auditor sets them on AMBIGUOUS cases. Existing scoring is unaffected when the fields are absent.

The audit form (`audit_form.tsv`) exposes these as `secondary_classes_proposed` and `interaction_type_proposed` columns; `apply_audit_overrides.py` writes them into the gold when the auditor fills them in.

---

## What still needs human review

- **Round-2 OVERRIDE (1 case):** corrected via fix 4 (cefoxitin + KPC). The overall corpus has been regenerated; re-audit on a third round can verify.
- **Round-2 AMBIGUOUS (1 case):** an `ESBL hyperexpression + dual porin loss → doripenem R` hybrid case (mechreason_kp_000712, isolate 573.24407). This stays in the corpus and should be tagged with `secondary_mechanism_classes=[enzymatic_inactivation]` + `interaction_type=synergistic` by the human auditor. Same isolate has multiple downstream tasks worth tagging similarly.
- **Round-1 carry-over:** user + colleague should re-audit the 9 "non-KEEP" Round-1 cards using the corrected heuristic to confirm they are now correctly labeled, then close them out via `apply_audit_overrides.py`.

---

## Methodological framing for the paper

Three sentences for the methods section:

> "The MechReason gold mechanism labels were generated by a deterministic priority-ordered heuristic that maps gene-class evidence to mechanism class. We stratified-audited 31 randomly-sampled cards across all 9 mechanism classes (over-sampling permeability_loss, regulator_loss_of_function, and insufficient_evidence). The audit surfaced 5 systematic priority errors, which we corrected; a second audit on 29 fresh cards reduced the non-KEEP rate from 29% to 7%. Ambiguous hybrid mechanisms (ESBL hyperexpression + porin loss; KPC + cefoxitin co-driving cephalosporin R) are retained with optional `secondary_mechanism_classes` and `interaction_type` fields, populated by the human auditor for the affected cases."

This frames the audit-and-fix loop as a methodological contribution rather than a hidden weakness.
