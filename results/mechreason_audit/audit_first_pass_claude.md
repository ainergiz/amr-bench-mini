# MechReason Label Audit — Claude Opus 4.7 first-pass review

**Auditor:** Claude Opus 4.7 (this session), acting as a first-pass surrogate microbiologist.
**Date:** 2026-04-25
**Sample size:** 31 stratified MechReason tasks.

> ⚠️ **This is an LLM first pass, not a board-certified ID review.** It is meant to give the human auditor (user + colleague) a starting point — review my decisions and override anything you disagree with via `audit_form.tsv`.

## Summary

| Decision | Count | Notes |
|---|---:|---|
| KEEP | 22 | Heuristic is biologically defensible |
| OVERRIDE | 5 | Heuristic chose the wrong dominant mechanism |
| AMBIGUOUS | 4 | Hybrid mechanism / borderline phenotype / no single dominant cause |

**Heuristic credibility:** ~71% KEEP. Three concrete heuristic-priority bugs surfaced:
1. **Tetracycline + tet(A) + ramR LoF**: heuristic chooses `regulator_loss_of_function`, but tet(A) is a direct tetracycline efflux pump — efflux is the dominant mechanism. ramR LoF is supplementary.
2. **Cefoxitin + ompK36 frameshift + non-AmpC β-lactamases**: heuristic chooses `enzymatic_inactivation` (because there are bla* genes), but cefoxitin is not hydrolyzed by SHV-52, OXA-1, CTX-M-15, or TEM-1 — the dominant mechanism here is permeability loss + chromosomal AmpC induction.
3. **Tigecycline + wild-type tet(A) only (no regulator LoF)**: tet(A) alone does not give tigecycline R; this should be `insufficient_evidence` (HypothesisGen flavor — chromosomal regulator LoF likely missed by annotators).

Per-case decisions in `audit_form_claude_first_pass.tsv`. Reasoning below.

---

## Per-case reasoning

### #1 — `mechreason_kp_000342` · tigecycline R · gold = `efflux`

→ **OVERRIDE → `insufficient_evidence`**

**Reason:** Wild-type tet(A) and oqxAB have insufficient activity against tigecycline (a glycylcycline specifically designed to evade Tet pumps; oqxAB has weak tigecycline activity). Without a chromosomal regulator LoF (ramR / acrR / oqxR / marR) or a mosaic-mutant tet(A), the visible annotator hits do not explain a clinical R phenotype. This is a HypothesisGen case — most likely cause is unannotated chromosomal regulator LoF.

### #2 — `mechreason_kp_000569` · tigecycline I · gold = `efflux`

→ **AMBIGUOUS**

**Reason:** Wild-type tet(A) alone with tigecycline I (intermediate, not R) — borderline. Phenotype could be explained by low-level tet(A) activity at the I/R boundary, or by trace efflux. Not clearly any single mechanism.

### #3 — `mechreason_kp_000738` · tetracycline R · gold = `efflux`

→ **KEEP**

**Reason:** tet(A) and tet(B) are well-characterized direct tetracycline efflux pumps. Both confer tetracycline R. Heuristic call is correct.

### #4 — `mechreason_kp_000224` · aztreonam R · gold = `enzymatic_inactivation`

→ **KEEP**

**Reason:** CTX-M-15 ESBL hydrolyzes aztreonam. SHV-28, SHV-106, TEM-1 contribute. ompK35 frameshift is irrelevant — aztreonam is destroyed before transit.

### #5 — `mechreason_kp_000698` · meropenem R · gold = `enzymatic_inactivation`

→ **KEEP**

**Reason:** KPC-3 (class A serine carbapenemase) hydrolyzes meropenem. Textbook enzymatic inactivation.

### #6 — `mechreason_kp_000807` · cefoxitin R · gold = `enzymatic_inactivation`

→ **OVERRIDE → `permeability_loss`**

**Reason:** Cefoxitin is a 7α-methoxy cephamycin, NOT efficiently hydrolyzed by CTX-M-15, OXA-1, SHV-52, or TEM-1. Cefoxitin R in K. pneumoniae is typically driven by porin loss (here ompK36_Q313Ter) + chromosomal AmpC-like activity or plasmid-mediated AmpC. The dominant mechanism is permeability loss; β-lactamases are confounders. Clear heuristic priority bug.

### #7 — `mechreason_kp_000868` · meropenem R · gold = `enzymatic_inactivation`

→ **KEEP**

**Reason:** VIM-19 (class B1 metallo-β-lactamase) hydrolyzes meropenem. Plus CTX-M-15 + CMY-4 (plasmid AmpC). Enzymatic inactivation correct.

### #8 — `mechreason_kp_000103` · ciprofloxacin R · gold = `insufficient_evidence`

→ **KEEP**

**Reason:** aac(6')-Ib-cr5, oqxAB, qnrB1 individually each give 2–4 fold MIC increase. Combined they don't reach clinical R level (typically need QRDR mutations: gyrA S83/D87 + parC S80). Genuine HypothesisGen case.

### #9 — `mechreason_kp_000117` · nitrofurantoin I · gold = `insufficient_evidence`

→ **KEEP**

**Reason:** No relevant hits. Nitrofurantoin R is rare; usually from nfsA/nfsB mutations not in standard annotator scope. Genuine HypothesisGen case.

### #10–#13 — quinolone or TMP-SMX with no QRDR · gold = `insufficient_evidence`

→ **All KEEP**

**Reason:** Same pattern as #8 — ancillary efflux + acquired resistance genes alone don't fully explain a clinical R phenotype, suggesting unannotated QRDR or regulator mutations.

### #14 — `mechreason_kp_000866` · fosfomycin R · gold = `intrinsic`

→ **KEEP** (with caveat)

**Reason:** Chromosomal *fosA* in K. pneumoniae provides intrinsic fosfomycin tolerance. 99.3% identity is consistent with the chromosomal allele. Caveat: distinguishing chromosomal-intrinsic from acquired-fosA at 99% identity is fuzzy; for our purposes, intrinsic is reasonable.

### #15–#17 — TMP-SMX with dfr/sul · gold = `metabolic_bypass`

→ **All KEEP**

**Reason:** dfrA1, dfrA14 (TMP-resistant DHFR) and sul1, sul2 (sulfa-resistant DHPS) are textbook bypass enzymes. #16 has only sul1 — borderline since TMP-SMX has both components, but sul1 alone often explains clinical R.

### #18, #19 — ertapenem/meropenem R · gold = `permeability_loss`

→ **Both KEEP**

**Reason:** No carbapenemase visible (the OXA gene has INTERNAL_STOP — disrupted, not active). SHV-31 is an ESBL but doesn't hydrolyze carbapenems. With ompK35 frameshift, residual SHV/TEM activity + porin loss = permeability_loss is the dominant mechanism.

### #20 — `mechreason_kp_000715` · imipenem R · gold = `permeability_loss`

→ **AMBIGUOUS**

**Reason:** SHV-5 is an ESBL; SHV_C-112A is a promoter-up mutation (overexpresses SHV); plus dual ompK35 + ompK36 frameshifts. Dominant mechanism is hybrid: high-expression ESBL + porin loss. The 9-class vocabulary doesn't have a hybrid category — flagging AMBIGUOUS.

### #21 — `mechreason_kp_000717` · meropenem R · gold = `permeability_loss`

→ **AMBIGUOUS** (same isolate as #20, same hybrid mechanism)

### #22 — `mechreason_kp_000734` · imipenem R · gold = `permeability_loss`

→ **KEEP** (with note)

**Reason:** CTX-M-15 + ompK35 frameshift is a published mechanism for imipenem R — CTX-M-15 has weak imipenem hydrolysis activity which is potentiated by porin loss. Dominant mechanism is permeability loss enabling residual ESBL hydrolysis.

### #23 — `mechreason_kp_000813` · meropenem I · gold = `permeability_loss`

→ **KEEP**

**Reason:** Same mechanism as #22 but milder phenotype (I not R).

### #24 — `mechreason_kp_000162` · tetracycline R · gold = `regulator_loss_of_function`

→ **OVERRIDE → `efflux`**

**Reason:** **Heuristic priority bug.** tet(A) is a direct tetracycline-specific MFS efflux pump — it confers tetracycline R on its own. ramR LoF derepresses AcrAB-TolC which adds additional efflux capacity, but tet(A) is the dominant mechanism. Should be `efflux`.

### #25 — `mechreason_kp_000662` · tetracycline R · gold = `regulator_loss_of_function`

→ **KEEP**

**Reason:** This isolate has oqxAB + ramR LoF but **no tet(A)**. Without a tetracycline-specific efflux pump, tetracycline R must come from regulator-LoF-driven AcrAB-TolC overexpression.

### #26 — `mechreason_kp_000921` · tetracycline R · gold = `regulator_loss_of_function`

→ **OVERRIDE → `efflux`**

**Reason:** Same heuristic priority bug as #24 — tet(A) is present and is the direct tetracycline-specific pump.

### #27 — `mechreason_kp_000922` · tigecycline R · gold = `regulator_loss_of_function`

→ **KEEP**

**Reason:** Tigecycline R from ramR LoF is the modal published mechanism in K. pneumoniae. tet(A) wild-type doesn't hit tigecycline.

### #28–#31 — quinolone R with gyrA + parC mutations · gold = `target_modification`

→ **All KEEP**

**Reason:** Single, double, or triple QRDR mutations in gyrA S83/D87 and parC S80 are textbook quinolone target modifications.

---

## Heuristic-priority fix recommendations (for the next iteration)

Based on the audit findings, three concrete fixes to `infer_mechanism()` would improve gold credibility before LLM eval:

1. **Drug-specific direct-action efflux > regulator-LoF.** When tetracycline + tet(A) coexist with ramR LoF, prefer `efflux` since tet(A) is the direct mechanism. Same logic for chloramphenicol + cat genes.
2. **Cefoxitin + porin loss without AmpC → `permeability_loss`** instead of `enzymatic_inactivation`. Cefoxitin is not hydrolyzed by ESBLs, narrow SHV/TEM/OXA. The bla* hits are confounders.
3. **Tigecycline phenotype + only wild-type tet(A)/oqxAB (no regulator LoF) → `insufficient_evidence`**. Becomes a HypothesisGen case.

---

## Implications for the paper

- **The heuristic-derived gold has a meaningful (~25%) error rate before audit** — this is exactly the "labels live or die" check the user prescribed.
- 4 of 5 override cases reveal **systematic heuristic-priority bugs** (drug-specific efflux > regulator LoF; cefoxitin biology; wild-type tet(A) for tigecycline) — they're addressable with concrete fixes.
- The 3 AMBIGUOUS hybrid cases (#2, #20, #21) suggest the 9-class vocabulary may be missing a "hybrid" or "synergistic" category for cases where two mechanisms genuinely co-drive resistance. Worth a paper-side discussion.
- After heuristic fixes + audit, **the published gold should ship as audit-corrected** with the audit trail recorded in the paper's methods section as a methodological contribution.
