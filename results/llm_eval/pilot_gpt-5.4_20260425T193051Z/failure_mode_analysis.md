# GPT-5.4 Pilot — Failure-Mode Analysis

**Run:** `pilot_gpt-5.4_20260425T193051Z`
**Provider/model:** OpenAI Responses API · gpt-5.4
**N tasks:** 50 (frozen MechReason pilot subset)
**Wall time:** ~20 min · **Cost:** ≈$1.75 estimated

## Headline numbers

| Metric | Value | Note |
|---|---:|---|
| Mechanism class accuracy | **74.0%** (37/50) | Composite: class + gene-family + layers |
| Parse-valid JSON | **100.0%** | Mechanical: `validate_output` checks generic field presence + types |
| Five-layer fields present | **100.0%** | Mechanical: each of `genome / protein / mechanism / cell / phenotype` is non-empty |
| Gene family correct | 84.0% | At least one required gene appears in agent's evidence |
| Mean evidence items per output | 5.28 |  |
| Parse / call errors | 0 |  |

> **Caveat on the two "100%" rows:** the current scorer is permissive — it confirms structural validity, not the depth of biological reasoning. In paper text these should be phrased as "parse-valid JSON" and "all five layer fields present," not "100% reasoning completeness."

## Per-class breakdown — three tiers emerge

| Tier | Class | n | correct | accuracy |
|---|---|---:|---:|---:|
| 🟢 perfect | `efflux` | 6 | 6 | **100%** |
| 🟢 perfect | `target_modification` | 7 | 7 | **100%** |
| 🟢 perfect | `regulator_loss_of_function` | 2 | 2 | **100%** |
| 🟡 strong | `enzymatic_inactivation` | 10 | 9 | 90% |
| 🟡 strong | `permeability_loss` | 10 | 8 | 80% |
| 🟡 ok | `metabolic_bypass` | 4 | 3 | 75% |
| 🔴 collapse | `insufficient_evidence` | 8 | 2 | **25%** |
| ⚠️ adjud. | `intrinsic` | 3 | 0 | **0%** *(gold-label ambiguity, see Pattern B)* |

> **The 0% on `intrinsic` is *not* the same kind of failure as the 25% on `insufficient_evidence`.** The former is a gold-label ontology disagreement (fosA is *both* intrinsic and enzymatic); the latter is genuine epistemic overconfidence on cases where annotator evidence does not explain the phenotype.

## The 13 failures cluster into 5 patterns

### Pattern A — HypothesisGen overconfidence (6 cases / 46% of failures) ⭐ HEADLINE

**Cases:** kp_000103, 000281, 000342, 000563, 000672, 000872

These are the gold = `insufficient_evidence` cases. GPT-5.4 systematically asserts a mechanism rather than recognizing the gap:

- 4 cases (quinolone R + qnr + aac(6')-Ib-cr + oqxAB, **no QRDR mutation** visible) → predicted `target_protection`. Mechanistically reasonable for *qnr alone*, but qnr only gives a 2–4 fold MIC bump — clinical R requires gyrA/parC mutations the annotator doesn't see. The agent should call `insufficient_evidence` + propose hypothesis "BLAST gyrA QRDR; expect S83/D87 substitution".
- 2 cases (tigecycline R + wild-type tet(A) + oqxAB) → predicted `efflux`. Wild-type tet(A) does not drive tigecycline R; the dominant cause is unannotated chromosomal regulator LoF.

**This is the central finding for the workshop's hypothesis-generation framing.** The agent's failure mode is *epistemic overconfidence* — when evidence is insufficient, it pattern-matches to the closest mechanism rather than flagging the gap. That is exactly what HypothesisGen is meant to detect.

### Pattern B — Gold-label ontology adjudication: fosA intrinsic-vs-enzymatic (3 cases)

**Cases:** kp_000357, 000866, 000896 — all fosfomycin R + chromosomal fosA in *K. pneumoniae*.

GPT-5.4 calls `enzymatic_inactivation` (fosA *is* a glutathione transferase that hydrolyzes fosfomycin). The heuristic gold calls `intrinsic` because fosA is chromosomal in *Klebsiella*. **Both are biologically defensible** — this is not a model error but a legitimate ontology disagreement: the resistance mechanism is enzymatic at the molecular level *and* intrinsic at the species level.

**Recommended action:** tag fosA-fosfomycin cases as `mechanism_class=intrinsic` + `secondary_mechanism_classes=[enzymatic_inactivation]` + `interaction_type=uncertain` via `apply_audit_overrides.py`. The 0% intrinsic accuracy disappears once we credit the secondary mechanism.

### Pattern C — Cefoxitin substrate-specificity gap (2 cases)

**Cases:** kp_000445, 000502 — cefoxitin R/I + ESBL/narrow-bla* + ompK frameshift, no AmpC, no carbapenemase.

GPT-5.4 predicts `enzymatic_inactivation`; gold (after audit) is `permeability_loss`. The agent doesn't reliably know that **CTX-M, narrow SHV, OXA-1 do not hydrolyze cefoxitin** — only AmpC family + KPC/NDM/VIM do. **Tool-augmentation candidate:** a CARD ARO substrate-specificity lookup that exposes which β-lactamase families act on cefoxitin would close this gap. This becomes the natural Day-4 tool-aug experiment.

### Pattern D — Folate vocabulary/schema ambiguity (1 case)

**Case:** kp_000701 — TMP-SMX R + dfrA12.

GPT-5.4 predicts `target_modification` (dfr replaces DHFR with a drug-insensitive variant — defensible). Gold says `metabolic_bypass` following classical microbiology pedagogy ("drug-insensitive alternate enzyme provides metabolic bypass of the drug-targeted enzyme"). Vocabulary disagreement, not knowledge gap.

**Recommended action:** clarify the prompt's mechanism-class vocabulary: `target_modification` = mutation of the chromosomal target; `metabolic_bypass` = acquired drug-insensitive enzyme (dfr, sul) that replaces the drug-sensitive native enzyme in the pathway.

### Pattern E — ArmA target_modification vs AME enzymatic_inactivation adjudication (1 case)

**Case:** kp_000830 — amikacin R + **armA** (16S rRNA methyltransferase, exact 100% hit) + aac(6')-Ib (partial contig-end, 88.1% cov) + aph(3')-VI (exact) + others.

GPT-5.4 predicts `target_modification` and gives a textbook-correct rationale: ArmA methylates the 16S rRNA aminoglycoside-binding site on the 30S ribosome → target modification. The heuristic gold says `enzymatic_inactivation` because the AME family-prefix check (`aac`/`aph`/`aad`/`ant`) fires first and there's no ArmA recognition.

**This is a heuristic priority bug + a hybrid case**, not a model error. The ribosome-methyltransferase family (ArmA, RmtA–H) confers high-level pan-aminoglycoside R via target modification; AMEs add complementary enzymatic inactivation. Correct gold should be `mechanism_class=target_modification` + `secondary_mechanism_classes=[enzymatic_inactivation]` + `interaction_type=additive`.

**Action:** add an ArmA/Rmt detection branch to `infer_mechanism()` ahead of the aminoglycoside-AME branch. Plus tag this case via `apply_audit_overrides.py`.

---

## Implications for the paper

The 74% headline number is fine, but the structure of the failure modes is the contribution.

Three insights that are paper-quality findings:

1. **Pattern A (HypothesisGen overconfidence) is the primary failure mode** — 6/13 errors and 75% of `insufficient_evidence` cases. GPT-5.4 prefers asserting a mechanism over flagging insufficient evidence. This validates HypothesisGen as a discriminating evaluation.

2. **Patterns B and E (fosA intrinsic-vs-enzymatic; ArmA target-vs-enzymatic) are gold-label adjudication cases, not model errors.** The user's hybrid-mechanism schema (`secondary_mechanism_classes` + `interaction_type`) handles them; the audit-fix-loop story now extends to a third round: LLM disagreement surfaces gold cases that need adjudication. **4/13 of the "errors" are cases where the model is biologically correct and the heuristic gold needs revision.**

3. **Pattern C (cefoxitin) defines a clean tool-augmentation experiment.** A CARD ARO substrate-specificity lookup is the experiment for "tool-augmented agent vs base agent" Day 4 baseline.

Once Patterns B + E are reclassified as gold-label adjudication and corrected via audit overrides, the **adjusted accuracy is 41/50 = 82%**, with the residual 18% concentrated in Pattern A (HypothesisGen overconfidence) and Pattern C (cefoxitin biology gap) — both directly addressable.

## Cost & latency footprint

- 50 tasks × ~22s/task wall time = ~18 minutes total
- Estimated cost: ~$1.75 (input ≈250K tokens × $2.50/1M, output ≈75K tokens × $15/1M) — exact token usage to be added in the next eval run via the manifest extension.

## Recommended next experiments

1. **Cross-vendor smoke + 20-task pilot on Claude Opus 4.7** — confirm the failure-mode taxonomy is model-family-invariant (the killer paper claim). ~$3.
2. **Tool-augmented variant on the same 50 tasks** — add a CARD ARO substrate-lookup tool to the agent harness; quantify lift on Pattern C cases. ~$3.
3. **Audit-override pass for Patterns B + E** — tag fosA and ArmA cases via `apply_audit_overrides.py`; recompute headline accuracy; show the audit-corrected number alongside the raw heuristic-gold number to demonstrate the audit-and-fix loop. Zero API cost.
4. **Full-corpus 924-task headline run on GPT-5.4** — defer until tool augmentation is added so the headline numbers reflect the final scaffold. ~$30–35.
5. **Carve out HypothesisGen sub-track** — the 24 `insufficient_evidence` tasks plus the 4 hybrid `permeability_loss` cases as a focused HypothesisGen benchmark with a separate scoring rubric (does the agent recognize the gap? does it propose a falsifiable hypothesis with a validation step?).
