# MechReason Hard Split — Category Taxonomy

This document defines the seven diagnostic categories that compose the 50-task
`mechreason_hard.jsonl` split. Each category targets a specific reasoning failure
mode that is invisible to gene-presence pattern matching: they require either
substrate-specificity biology, evidence-sufficiency judgment, mechanism/ontology
disambiguation, or primary/secondary mechanism reasoning. Positive controls are
included so the split cannot be solved by uniform abstention.

The split was constructed deterministically from the full 924-task corpus via
`scripts/build_hard_subset.py`. Selection rules and per-task IDs are recorded in
`results/mechreason_hard_summary.json`.

## 1. `hypothesisgen_insufficient_evidence` (n = 24)

**What it tests.** Whether the model recognizes that the visible annotation
evidence does not deterministically explain the observed clinical resistance
phenotype, and outputs `insufficient_evidence` rather than the closest plausible
acquired mechanism.

**Biological rationale.** Tigecycline is a glycylcycline rationally designed to
evade *tet* efflux pumps. Wild-type *tet(A)* and *oqxAB* without
loss-of-function mutations in their cognate regulators (*ramR, acrR, oqxR,
marR*) cannot drive a clinical-R MIC for tigecycline. Likewise, *qnrA/B/S* alone
typically yields ciprofloxacin MICs in the susceptible-to-intermediate range;
clinical R requires accumulated *gyrA/parC* QRDR mutations or efflux
hyper-expression. In each task, the AST records resistance and the visible
annotators report a gene that is name-suggestive but mechanistically
insufficient.

**Why it discriminates models.** The correct call is `insufficient_evidence`
plus a falsifiable hypothesis (e.g., screen for *ramR* LoF, sequence the QRDR,
phenotype additional resistance markers). Pattern-matching agents collapse to
the closest mechanism in the gene's name (`qnr → target_protection`,
`tet(A) + oqxAB → efflux`) and over-attribute phenotype to insufficient
evidence. This category isolates *epistemic abstention* from *mechanism naming*.

## 2. `intrinsic_acquired_ontology` (n = 3)

**What it tests.** Whether the model distinguishes the molecular mechanism from
the acquisition status when the resistance vocabulary conflates them.

**Biological rationale.** *fosA* in *K. pneumoniae* is a chromosomally encoded,
constitutively expressed glutathione-S-transferase that conjugates fosfomycin
under Mn²⁺/K⁺. The molecular mechanism is enzymatic inactivation; the
acquisition status is intrinsic. Heuristic gold initially labeled these as
`intrinsic`. Audit-adjusted gold (after tri-vendor convergence on
`enzymatic_inactivation`) labels them by mechanism class with the intrinsic
status preserved as an annotation.

**Why it discriminates models.** This category is reported in both **strict**
and **adjudicated** forms. Strict scoring rewards the heuristic vocabulary
choice; adjudicated scoring rewards molecular-mechanism reasoning. The category
is retained in the hard split as a category label even when its members no
longer share a single gold class — it isolates a vocabulary-versus-biology
disagreement that is invariant across vendors.

## 3. `regulator_lof_vs_direct_efflux` (n = 2)

**What it tests.** Whether the model distinguishes regulator loss-of-function
(de-repression of an efflux pump) from direct drug-specific efflux as the
primary mechanism, when both could in principle be invoked.

**Biological rationale.** *ramR* loss-of-function de-represses the *ramA-acrAB-
tolC* axis, raising MICs for multiple antibiotic classes. When tigecycline R is
attributable specifically to AcrAB hyper-expression downstream of *ramR* LoF,
the dominant mechanism is `regulator_loss_of_function`, not `efflux`. Direct
*tet(A)*-driven efflux requires substrate-active *tet* variants and is
insufficient for tigecycline.

**Why it discriminates models.** The category requires causal-chain reasoning,
not surface-feature pattern matching. Models that flatten regulator loss to
generic efflux miss the intended distinction.

## 4. `hybrid_porin_beta_lactamase` (n = 4)

**What it tests.** Whether the model assigns the dominant primary mechanism in
cases where two mechanisms genuinely co-drive resistance.

**Biological rationale.** All four cases are isolate 573.24407, which carries
SHV-5 ESBL plus a SHV upstream promoter-up substitution (hyper-expression) and
dual ompK35/ompK36 frameshifts. The combination produces carbapenem R via
permeability loss as the primary trigger and residual SHV hydrolysis as a
synergistic secondary contribution. The schema's optional
`secondary_mechanism_classes` and `interaction_type` fields capture this.

**Why it discriminates models.** Models that assign `enzymatic_inactivation`
based on the visible β-lactamase miss that ESBLs cannot hydrolyze carbapenems
without porin co-loss; models that abstain miss the resolved mechanistic story.
The correct answer is `permeability_loss` primary, `enzymatic_inactivation`
secondary, `synergistic` interaction.

## 5. `cefoxitin_substrate_decoy` (n = 10)

**What it tests.** Whether the model rejects mechanism-suggestive β-lactamases
that cannot in fact hydrolyze the target antibiotic.

**Biological rationale.** Cefoxitin is a 7α-methoxy cephamycin. ESBLs (CTX-M
family), narrow-spectrum SHV/TEM, and OXA-1 do *not* efficiently hydrolyze it.
The dominant cefoxitin-R mechanism in this isolate set is OmpK35/OmpK36 porin
loss; visible non-AmpC, non-carbapenemase β-lactamases are confounders. AmpC
family (ACT, DHA, MIR), KPC carbapenemases, and metallo-β-lactamases (NDM, VIM,
IMP) *can* hydrolyze cefoxitin and are explicitly excluded from this category
(see *cefoxitin_true_hydrolysis_control*).

**Why it discriminates models.** Cefoxitin is a substrate-specificity test for
β-lactamase biology. Pattern-matching agents collapse "Resistant + visible
β-lactamase" to `enzymatic_inactivation`. The correct answer is
`permeability_loss`. This is the single category where vendor knowledge gaps in
β-lactam substrate biology surface most starkly: in our pilot, GPT-5.4 solved
4/10, Gemini 3.1 Pro and Claude Opus 4.7 solved 10/10.

## 6. `drug_specificity_positive_control` (n = 4)

**What it tests.** Whether the model correctly assigns mechanism when the visible
evidence *is* sufficient for the target drug, in cases paired by isolate to
*hypothesisgen_insufficient_evidence* tigecycline cases on the same isolate.

**Biological rationale.** Wild-type *tet(A)* + *oqxAB* without regulator LoF
*can* explain a tetracycline R MIC (mechanism: `efflux`), even though the same
gene profile cannot explain tigecycline R. Each task here is mated to a
tigecycline insufficient-evidence task on the same isolate via
`hard_split.paired_task_id`.

**Why it discriminates models.** The pairing exposes whether the model
genuinely reasons about drug-specific substrate sensitivity or simply names the
most prominent visible gene. A model that calls `efflux` on both the
tetracycline and tigecycline tasks is right by accident on tetracycline and
wrong on tigecycline; only a model that varies its call across the pair
demonstrates substrate-aware reasoning.

## 7. `cefoxitin_true_hydrolysis_control` (n = 3)

**What it tests.** Positive control for substrate-specificity reasoning: when
the visible β-lactamase *can* hydrolyze cefoxitin, the gold mechanism is
`enzymatic_inactivation`.

**Biological rationale.** AmpC family enzymes (CMY, ACT, DHA, MIR), KPC
carbapenemases, and NDM/VIM metallo-β-lactamases all hydrolyze cefoxitin
efficiently. The split includes one representative of each: KPC (kp_000046),
NDM (kp_000258), CMY/AmpC (kp_000610). These tasks are the contrastive mate to
*cefoxitin_substrate_decoy* and prevent a model from solving the decoy category
trivially by always answering `permeability_loss` on cefoxitin tasks.

**Why it discriminates models.** A model that systematically abstains or
defaults to `permeability_loss` on cefoxitin tasks loses on this control;
a model that systematically defaults to `enzymatic_inactivation` on visible
β-lactamases loses on the decoy. Solving both requires the substrate-specific
distinction.

---

## Reporting convention

Per-category accuracy is reported only where n ≥ 10 (see
`results/headline_table.md`). Categories with n ≤ 5 are reported descriptively
without confidence intervals; their role in the split is to provide
contrastive controls and ontology stress tests, not to support
population-level claims.

The `intrinsic_acquired_ontology` category is reported with both strict and
adjudicated accuracy, since the audit moved its three members from `intrinsic`
to `enzymatic_inactivation`. All other categories are stable across strict and
adjudicated scoring.
