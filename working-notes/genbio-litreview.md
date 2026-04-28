# GenBio @ ICML 2026 — Lit Review Synthesis & Paper Angles

**Compiled:** 2026-04-25 · **Deadline:** 2026-05-01 AOE (6 days) · **Author constraints:** in-silico only, no wet-lab access, no proprietary data, agent-orchestration on top of frontier APIs · **Domain:** infectious diseases / AMR / antibiotic discovery

---

## TL;DR

The agentic-bio field crystallized in the past 12 months around a recognizable architectural template (planner + tools + critic + optional self-evolution / wet-lab loop). The two highest-impact published systems for our angle are:

- **SAGA** (Du, …, **Wengong Jin** et al., Dec 2025) — bi-level objective-evolving agent, **already demonstrated wet-lab-validated novel antibiotic against *E. coli***. **Jin is a GenBio 2026 organizer.**
- **Google AI Co-scientist** (Feb 2025) — Gemini multi-agent system, **already demonstrated novel AMR mechanism rediscovery** with Imperial College.

Plus **Fleming** (Apr 2025, Mtb antibiotic design, multi-agent), **Robin** (FutureHouse, May 2025, dAMD wet-lab loop), and **The Virtual Lab** (Zou lab, Nature 2025, nanobody wet-lab loop). All co-authored by people the workshop reviewers know well.

**The unambiguous gap given our constraints:** there is **no public AMR-specific agent benchmark** across the multiple sub-tasks ID people care about (genotype→phenotype, mechanism reasoning, stewardship, outbreak investigation, novel antibiotic design). All major bio-agent benchmarks (LAB-Bench, BixBench, Biomni-Eval1, ScienceAgentBench, CompBioBench, BioAgent Bench, scBench) have zero AMR coverage.

**Strongest single-paper contribution we can ship by May 1 in silico:** an open AMR agent benchmark + a critical evaluation of 3–4 frontier biomedical agents on it.

---

## Master paper map (top citations across 4 streams)

### A. Agentic-bio landmarks (must-cite + position against)
- **Coscientist** (Boiko, *Nature* 2023) — first LLM agent + cloud-lab loop
- **ChemCrow** (Bran, *NMI* 2024) — canonical LLM + chemistry tools
- **BioDiscoveryAgent** (Roohani, ICLR 2025) — agent beats BO at CRISPR design — **Roohani = GenBio organizer**
- **CRISPR-GPT** (Qu, *Nat. Biomed. Eng.* 2025) — withholding code for biosecurity — relevant precedent for AMR
- **Biomni** (Huang, bioRxiv 2025) — generalist biomedical agent, 150 tools / 59 DBs / 25 subfields — natural baseline
- **STELLA** (Jin, Zhang, Cong 2025) — self-evolving toolset, beat Biomni on multimodal eval
- **The Virtual Lab** (Swanson, *Nature* 2025) — PI + specialists + critic, nanobody wet-lab — **Zou = GenBio invited speaker**
- **Robin** (FutureHouse 2025) — autonomous dAMD wet-lab loop
- **Lab-in-the-Loop** (Genentech 2025) — industrial closed-loop antibody platform
- **The AI Scientist v2** (Sakana, ICLR 2025) — workshop-paper-passing autonomous research
- **SAGA** (Du, **Jin** et al., Dec 2025) — bi-level objective evolution; **antibiotic + nanobody + DNA enhancers wet-lab validated**
- **Google AI Co-scientist** (Feb 2025) — generate-debate-evolve, **AMR mechanism rediscovery**
- **TxAgent** (Zitnik 2025) — fine-tuned 8B + 211 tools, drug reasoning
- **AlphaFold 3** (DeepMind 2024) — non-agentic generative anchor

### B. Antibiotic / antimicrobial discovery work
- **Fleming** (Wei et al., bioRxiv Apr 2025) — 4-agent system for Mtb, 83% in-vitro hit rate — closest published precedent
- **AMP-Designer** (Tencent, *Sci Advances* 2025) — LLM-foundation AMP design, mouse-validated
- **ApexAmphion** (de la Fuente, bioRxiv Sep 2025) — 6.4B PLM + PPO, AMP design SOTA
- **SyntheMol-RL** (Stokes/Zou labs, *Mol Syst Biol* 2026) — synthesizable small-molecule antibiotic generation, MRSA-validated
- **SPEL/ProteoGPT** (*Nature Microbiology* 2025) — pipeline-ensembled LLMs, MDR-validated
- **Halicin / Abaucin / Wong et al.** (Stokes/Collins labs, 2020/2023/2024) — foundational AI-discovered antibiotics

### C. AMR detection & FM/agent work
- **AMRscope** (Sanger, bioRxiv Sep 2025) — ESM-2 + MLP for AMR variant prediction — closest "ESM-AMR" precedent
- **LLMTB** (PMC 2025) — LLM for TB resistance, 13 drugs, novel mechanism discovery
- **ESMARG** (*Frontiers Microbio* 2025) — ESM-1b + ProtBert ARG predictor, F1=0.97
- **METAGENE-1** (2025) — 7B metagenomic FM trained on wastewater
- **Yoo et al.** (Drexel) — DNA-LM + BioBERT ensembles for ARG prediction
- **AMR-GNN** (*Nat Comm* 2026) — multi-representation GNN for *P. aeruginosa* AMR
- **TB-DROP / CRyPTIC ML** (2024) — DL on whole-genome MTB mutations

### D. Stewardship & clinical AMR agents (no agent has all this)
- **COMPOSER-LLM** (UCSD/Nemati, *npj Digital Med* 2025) — LLM + structured-data sepsis
- **AHRQ Sepsis Phenotypes + AMR** (2024–26) — Llama-3 over H&P notes for AMR risk
- **KINBIOTICS** (*JMIR Human Factors* 2025) — sepsis CDSS with HFE eval
- **TxAgent** (above) — drug reasoning

### E. Benchmarks (no AMR-specific track exists)
- **LAB-Bench** (FutureHouse 2024) — 2,400+ MCQs, biology research
- **BixBench** (FutureHouse 2025) — bioinformatics in Jupyter, 53 capsules
- **Biomni-Eval1** (Stanford 2025) — 433 instances, 10 reasoning tasks
- **ScienceAgentBench / MLAgentBench / MLE-bench / PaperBench / SciCode / AstaBench** — general scientific agents
- **BioPlanner / BioProBench** — protocol planning
- **GenoTEX / GeneBench / BioReason / BioML-bench / CompBioBench** — genomics & biomedical ML
- **CRISPR-GPT eval / MedAgentBench / MedAgentsBench / HIVMedQA / TRINDs / WMDP-Bio** — clinical / safety
- **TDC / PharmaBench / ChemBench** — drug discovery

### F. Position / skeptical papers (must cite to avoid looking naive)
- **From AI for Science to Agentic Science** (survey 2025) — adopt this taxonomy
- **AI agents for biological research** survey (*Briefings in Bioinformatics* 2026) — 5D taxonomy of 115 agents
- **Why LLMs Aren't Scientists Yet** (2026) — empirical critique of failure modes
- **Evaluating Sakana's AI Scientist** (Beel et al. 2025) — 42% experiment failure rate, hallucinated results
- **Multi-agent AI systems need transparency** (*Nat Mach Intell* 2026)
- **James Zou — Lancet commentary on agentic AI teammates in medicine** (Feb 2026) — **organizer reading**

### G. Datasets we can use (all public)
- **CARD** (McMaster, *NAR* 2023) — 6,442 reference sequences, RGI software, ARO ontology
- **AMRFinderPlus / NDARO** (NCBI) — production AMR annotation tool
- **MEGARes 3.0** (*NAR* 2023) — 8,733 ARG accessions, hierarchy-friendly
- **ResFinder / Kleborate** — alternative annotators
- **BV-BRC / PATRIC** — ~67,800 bacterial genomes with paired AST data
- **CRyPTIC** — 12,000–35,000+ MTB isolates with WGS+DST
- **NCBI Pathogen Detection** — outbreak clusters
- **PLSDB 2025** — 72,360 plasmids
- **AMPSphere** — 863,498 candidate AMPs from 87,920 genomes + 63,410 metagenomes
- **TDC** — HIV inhibition prediction subset
- **Stokes-lab / Wong et al. screens** — held-out actives for novel-antibiotic eval

---

## The competitive landscape (the hard truth)

The "agentic AI for antibiotic discovery" thesis is no longer white space:

- **SAGA** already shipped a wet-lab-validated novel antibiotic against *E. coli* with bi-level objective evolution. Wengong Jin is a GenBio organizer.
- **Fleming** already shipped a multi-agent system for Mtb antibiotic design with 83% in-vitro hits.
- **Google AI Co-scientist** already demonstrated novel AMR mechanism rediscovery at Imperial.
- **AMP-Designer / SPEL / ApexAmphion** already shipped LLM/PLM-driven AMP design with mouse models.
- **The Virtual Lab + Robin** are the templates for "wet-lab-validated agent" — neither did antibiotics, but both will be reviewers' anchors.

**Without a wet lab, we cannot beat this on "build a better antibiotic agent."** That door is closed for May 1.

What remains:

1. **Evaluation / benchmark contributions** — no public AMR agent benchmark exists. Clean white space.
2. **Critical / honest-failure-mode evaluations** of existing agents on AMR tasks. The "Why LLMs Aren't Scientists Yet" energy is welcome at GenBio (organizers want field maturation).
3. **Architectural deltas that don't require wet-lab** — e.g., resistance-evolution adversary, database-disagreement reconciliation, calibrated uncertainty.
4. **Domain-vertical agent without claiming wet-lab validation** — clearly framed as a methods/tooling paper, with strong public-data eval.

---

## Recurring architectural pattern (the template every paper now references)

> **Planner / PI → Tool router → Domain tools (computational + simulators + databases [+ wet-lab APIs]) → Memory (scratchpad + episodic results store) → Critic / Reviewer → (optional) Self-evolution layer → (optional) Human-in-the-loop checkpoint.**

Differentiation axes (pick yours consciously):
- **Multi-agent role-play** (PI + specialists + critic, à la Virtual Lab, MedAgents, AI Co-scientist) **vs single-controller-with-verification** (GeneAgent, BioDiscoveryAgent)
- **Curated expert toolset** (ChemCrow, Biomni-E1, TxAgent's ToolUniverse) **vs self-evolving toolset** (STELLA's Tool Ocean)
- **Generate-debate-evolve / Elo tournaments** (AI Co-scientist, Lab-in-the-Loop) **vs iterative reflection scratchpads** (BioDiscoveryAgent)
- **Prompting frontier models vs RL-fine-tuned small open models** (Aviary, TxAgent)
- **Closed-loop wet-lab vs dry-lab-only**
- **Shared cumulative knowledge** (AgentRxiv) **vs isolated runs**

---

## Five candidate paper angles, ranked by feasibility-by-May-1

Each angle: pitch · novelty · feasibility · what we'd build · risks.

### 🥇 Angle 1 — **AMR-Bench: An open benchmark for agentic AMR systems, with critical evaluation of frontier biomedical agents**

**Pitch:** First open benchmark for AI agents on AMR-specific tasks. Five tracks: (1) **GenoPheno** — genotype→phenotype prediction with mechanism rationale (paired WGS+AST from BV-BRC); (2) **DBReconcile** — agent must reconcile disagreements across CARD / AMRFinderPlus / MEGARes / ResFinder for the same isolate (10–30% disagreement, documented gap); (3) **EmpiricRx** — empiric-therapy recommendation from synthetic patient + culture report + local antibiogram; (4) **ResistomeMine** — agent finds emerging ARG/MGE combinations in metagenomes; (5) **NovelAB-Triage** — agent triages a chemical library against a target pathogen using public tools. We then evaluate **Biomni, Virtual Lab, Google AI Co-scientist (or open replication), and a vanilla GPT-5 ReAct agent** on the benchmark, document failure modes, propose a small AMR-specific scaffold that improves on the baselines.

**Novelty:** ⭐⭐⭐⭐⭐ — no public AMR-specific agent benchmark exists; convergent finding from Streams 2 and 4.

**Feasibility:** ⭐⭐⭐⭐ — public data exists for tracks 1, 2, 3, 4; track 5 uses TDC/ChEMBL. ID expertise is the moat for rubric design. Eval = run 4 agents on N tasks; 6 days is tight but doable for a 4-page short paper if we cut tracks to 2 or 3. 9-page long paper if we hit all five.

**What we'd build:**
- A Docker image with CARD/RGI, AMRFinderPlus, MEGARes, ResFinder, BLAST, snippy preinstalled
- A small dataset per track (50–200 tasks/track), 80/20 public/held-out split, OpenReview-friendly
- A Python evaluation harness (pass/fail or VME/ME for track 1)
- 1–2 baseline agents (vanilla ReAct + a Biomni-extended agent) and benchmark numbers for ≥2 frontier agents
- A GitHub repo + a leaderboard page (HAL-style)
- Honest failure-mode taxonomy (what breaks: hallucinated genes, incorrect tool calls, etc.)

**Risks:**
- AMR community has clinical-microbiology standards (CLSI/EUCAST) we must respect — wrong rubric design = nontrivial reject signal
- Frontier-agent evaluation costs API tokens; budget needed
- 2 of the 5 tracks might be cut for time

**Why this wins for GenBio reviewers:** hits CFP topic 4 (benchmarks/evaluation) explicitly, addresses topic 6 (safety/governance) via biosecurity guardrails, doesn't claim wet-lab results we can't deliver, and the "honest failure-mode evaluation" framing aligns with workshop-organizer skepticism (Zou's Lancet piece, "Why LLMs Aren't Scientists Yet").

---

### 🥈 Angle 2 — **The Resistome-Reconciliation Agent: Tool-using agent for AMR annotation across disagreeing databases**

**Pitch:** A focused agent paper. CARD, AMRFinderPlus, MEGARes, ResFinder, NDARO disagree on **10–30% of annotations on the same isolate** (documented in *npj AMR* 2025). We build an LLM agent that calls all five, reads ARO ontology + literature evidence, and outputs a single calibrated annotation with confidence scores and citations. Eval against held-out phenotype data.

**Novelty:** ⭐⭐⭐⭐ — the disagreement problem is documented but no agent paper has tackled it.

**Feasibility:** ⭐⭐⭐⭐⭐ — narrow scope, single artifact, all public data, clean evaluation (concordance + AST). Most likely to actually finish.

**What we'd build:** Agent + ARO retrieval + simple eval harness on ~500 annotated isolates. 4-page paper.

**Risks:** Smaller scope = less impact than Angle 1; reviewers might say "neat tool but where's the science?" Mitigation: lean into the calibration and uncertainty story (conformal prediction over agent ensembles is open territory).

---

### 🥉 Angle 3 — **Red Team for Antibiotic Agents: Resistance-evolution adversaries in agentic antibiotic design**

**Pitch:** Architectural delta over SAGA / Fleming. Existing agents optimize MIC + toxicity; **none model the resistance-evolution adversary**. We bolt a Red Team agent onto an existing antibiotic-design loop (SyntheMol-RL or AMP generator). Red Team simulates resistance evolution against each candidate (mutational scan via ESM-2 / AMRscope-style scoring; cross-resistance lookup against CARD/ResFinder; published literature on MoA-class resistance). The design loop's reward becomes (potency − resistance_susceptibility). Eval: in-silico resistance-evolution rate of selected candidates vs SAGA/SyntheMol-RL baseline; recall on held-out clinically known cross-resistance pairs.

**Novelty:** ⭐⭐⭐⭐ — the resistance-aware framing has not appeared in any agentic-bio paper to date (cross-checked Streams 1, 3).

**Feasibility:** ⭐⭐⭐ — needs a generator + a simulator + careful eval setup. 6 days is tight; would have to lean heavily on ApexAmphion or SyntheMol-RL as a frozen tool.

**What we'd build:** Two-agent system (Designer + Red Team) on top of an open generator; in-silico resistance simulator; comparison plot. 4–9 pages.

**Risks:** "Resistance-evolution simulator" is itself a research question; we'd need to use an off-the-shelf proxy (AMRscope, ESM-2 mutational scan) and be honest about limitations. SAGA might quietly include this in updates we don't see.

---

### Angle 4 — **Stewardship-Agent: EHR + Genomic Multimodal AMR Decision Support**

**Pitch:** Combine COMPOSER-LLM-style EHR reasoning + AMRscope-style genomic prediction in one agent. Reads (synthetic) H&P + culture report + WGS isolate → predicts MIC + resistome → reasons over local antibiogram + allergies → proposes therapy. Convergent gap from Stream 2: **no agent combines EHR and genomic AMR**.

**Novelty:** ⭐⭐⭐⭐ — clean integration story, first agent of its kind.

**Feasibility:** ⭐⭐ — needs synthetic EHR data, antibiogram corpus, and clinical-rubric eval. We'd need an ID-physician collaborator to design rubrics; otherwise reviewers will flag clinical validity. Tight for 6 days.

**Risks:** Regulatory / clinical credibility; without ID expert review of the rubric this won't pass review.

---

### Angle 5 — **Pure Position/Skepticism Paper: "What agentic AI for biology gets wrong about AMR"**

**Pitch:** A 4-page critical position paper. Take the Google AI Co-scientist AMR result, Fleming's Mtb hit rate, SAGA's antibiotic claim — examine what was actually demonstrated (and what wasn't) under a clinical-microbiology lens. Identify three specific failure modes (e.g., Mtb's 83% in-vitro hit rate doesn't translate to clinically meaningful potency; AMR mechanism rediscovery ≠ novel discovery). Propose what a rigorous claim looks like (held-out post-cutoff isolates; CLSI/EUCAST-aligned metrics; resistance-evolution bench).

**Novelty:** ⭐⭐⭐ — the field is hungry for honest critiques; "Why LLMs Aren't Scientists Yet" (2026) is a precedent. But position-only papers rarely win at applied workshops.

**Feasibility:** ⭐⭐⭐⭐⭐ — pure writing, no system, 6 days easy.

**Risks:** GenBio reviewers may want a system contribution. Lower acceptance probability than Angles 1–3.

---

## Recommendation

**Angle 1 (AMR-Bench)** is the highest-leverage single paper given our constraints, deadline, and the fact that no published work has occupied that bench. If we trim to **3 tracks** (GenoPheno + DBReconcile + EmpiricRx) we can credibly ship a 4-page paper by May 1; with 5 tracks and stronger baselines, a 9-page long paper is plausible if we move fast.

**Backup if Angle 1 looks too big in 24h of scoping:** drop to **Angle 2 (DBReconcile only)** as a clean, finishable, well-scoped contribution. Reviewers will respect a tight paper that does one thing well.

**Stretch:** combine Angle 1 + an Angle-3-flavored "AMR-aware scaffold" mini-baseline, demonstrating that an off-the-shelf Biomni + AMR tools beats vanilla Biomni on the benchmark — that's a legitimate methods contribution layered on top.

---

## Source links (deduped, curated)

### Landmark systems
- [Coscientist (Nature 2023)](https://www.nature.com/articles/s41586-023-06792-0) · [ChemCrow (NMI 2024)](https://www.nature.com/articles/s42256-024-00832-8) · [code](https://github.com/ur-whitelab/chemcrow-public)
- [BioDiscoveryAgent (ICLR 2025)](https://arxiv.org/abs/2405.17631) · [code](https://github.com/snap-stanford/BioDiscoveryAgent)
- [CRISPR-GPT (Nat. Biomed. Eng. 2025)](https://www.nature.com/articles/s41551-025-01463-z)
- [Biomni (bioRxiv 2025)](https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1) · [code](https://github.com/snap-stanford/Biomni)
- [STELLA (arXiv 2025)](https://arxiv.org/abs/2507.02004)
- [The Virtual Lab (Nature 2025)](https://www.nature.com/articles/s41586-025-09442-9) · [code](https://github.com/zou-group/virtual-lab)
- [Robin (arXiv 2025)](https://arxiv.org/abs/2505.13400) · [code](https://github.com/Future-House/robin)
- [Lab-in-the-Loop (bioRxiv 2025)](https://www.biorxiv.org/content/10.1101/2025.02.19.639050v1)
- [The AI Scientist v2 (ICLR 2025)](https://arxiv.org/abs/2504.08066)
- [SAGA (arXiv 2025)](https://arxiv.org/abs/2512.21782)
- [Google AI Co-scientist (arXiv 2025)](https://arxiv.org/abs/2502.18864)
- [TxAgent (arXiv 2025)](https://arxiv.org/abs/2503.10970) · [project](https://zitniklab.hms.harvard.edu/TxAgent/)
- [AlphaFold 3 (Nature 2024)](https://www.nature.com/articles/s41586-024-07487-w)

### Antibiotic / AMP discovery
- [Fleming (bioRxiv 2025)](https://www.biorxiv.org/content/10.1101/2025.04.01.646719v2)
- [AMP-Designer (Sci Adv 2025)](https://www.science.org/doi/10.1126/sciadv.ads8932)
- [SPEL (Nat Microbiol 2025)](https://www.nature.com/articles/s41564-025-02114-4)
- [ApexAmphion (bioRxiv 2025)](https://www.biorxiv.org/content/10.1101/2025.09.23.678086v1.full)
- [SyntheMol-RL (bioRxiv 2025)](https://www.biorxiv.org/content/10.1101/2025.05.17.654017v1) · [code](https://github.com/swansonk14/SyntheMol)
- [SyntheMol (NMI 2024)](https://www.nature.com/articles/s42256-024-00809-7)
- [Halicin (Cell 2020)](https://www.sciencedirect.com/science/article/pii/S0092867420301021)
- [Wong et al. (Nature 2024)](https://www.nature.com/articles/s41586-023-06887-8)
- [AMPSphere (Cell 2024)](https://pubmed.ncbi.nlm.nih.gov/38843834/)

### AMR detection / FM
- [AMRscope (bioRxiv 2025)](https://www.biorxiv.org/content/10.1101/2025.09.12.672331v1.full)
- [LLMTB (PMC 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12261485/)
- [ESMARG (Frontiers Microbio 2025)](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2025.1628952/full)
- [METAGENE-1 (arXiv 2025)](https://arxiv.org/abs/2501.02045) · [HF](https://huggingface.co/metagene-ai/METAGENE-1)
- [AMR-GNN (Nat Comm 2026)](https://www.nature.com/articles/s41467-026-69934-8)
- [Yoo et al. (arXiv 2024/2025)](https://arxiv.org/abs/2401.00642) · [follow-up](https://arxiv.org/html/2503.04413v1)

### Stewardship / clinical AMR
- [COMPOSER-LLM (npj Digital Med 2025)](https://www.nature.com/articles/s41746-025-01689-w)
- [AHRQ Sepsis + AMR](https://digital.ahrq.gov/ahrq-funded-projects/identifying-sepsis-phenotypes-associated-antibiotic-resistant-pathogens-using)
- [LLM CDSS in 16 specialties (Cell Reports Med 2025)](https://www.cell.com/cell-reports-medicine/fulltext/S2666-3791(25)00396-9)
- [LLMs for stewardship review (npj AMR 2025)](https://www.nature.com/articles/s44259-025-00084-5)

### Benchmarks
- [LAB-Bench (arXiv 2024)](https://arxiv.org/abs/2407.10362) · [code](https://github.com/Future-House/LAB-Bench)
- [BixBench (arXiv 2025)](https://arxiv.org/abs/2503.00096) · [code](https://github.com/Future-House/BixBench)
- [Biomni-Eval1 (above)](https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1)
- [ScienceAgentBench (arXiv 2024)](https://arxiv.org/abs/2410.05080) · [code](https://github.com/OSU-NLP-Group/ScienceAgentBench)
- [BioPlanner (arXiv 2023)](https://arxiv.org/abs/2310.10632) · [BioProBench](https://arxiv.org/abs/2505.07889)
- [AstaBench (Allen AI 2025)](https://arxiv.org/abs/2510.21652) · [code](https://github.com/allenai/asta-bench)
- [CompBioBench (bioRxiv 2026)](https://www.biorxiv.org/content/10.64898/2026.04.06.716850v1.full)
- [TDC](https://tdcommons.ai/) · [PharmaBench / Mozi](https://arxiv.org/html/2603.03655v1) · [ChemBench (Nat Chem 2025)](https://www.nature.com/articles/s41557-025-01815-x)

### Position / skeptical
- [From AI for Science to Agentic Science (survey 2025)](https://arxiv.org/abs/2508.14111)
- [AI agents for biological research survey (BiB 2026)](https://academic.oup.com/bib/article/27/1/bbag075/8499367)
- [Why LLMs Aren't Scientists Yet (2026)](https://arxiv.org/abs/2601.03315)
- [Evaluating Sakana's AI Scientist (2025)](https://arxiv.org/abs/2502.14297)
- [Multi-agent AI systems need transparency (Nat Mach Intell 2026)](https://www.nature.com/articles/s42256-026-01183-2)
- [James Zou — Lancet on AI teammates (2026)](https://dbds.stanford.edu/james-zou-the-rise-of-agentic-ai-teammates-in-medicine-the-lancet-2-8-issue/)

### Datasets
- [CARD (NAR 2023)](https://academic.oup.com/nar/article/51/D1/D690/6764414) · [card.mcmaster.ca](https://card.mcmaster.ca/)
- [AMRFinderPlus](https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/)
- [MEGARes 3.0 (NAR 2023)](https://academic.oup.com/nar/article/51/D1/D744/6830666)
- [BV-BRC AMR (BiB 2021)](https://academic.oup.com/bib/article/22/6/bbab313/6347947)
- [CRyPTIC](https://www.crypticproject.org/)
- [PLSDB 2025 (NAR)](https://academic.oup.com/nar/article/53/D1/D189/7905312)
- [AMR databases comparison (npj AMR 2025)](https://www.nature.com/articles/s44259-025-00169-1)

### Workshop
- [GenBio @ ICML 2026 CFP](https://genbio-workshop.github.io/2026/)
- [OpenReview](https://openreview.net/group?id=ICML.cc/2026/Workshop/GenBio)
- [Overleaf template](https://www.overleaf.com/read/dnjfbdnypxwn#79923f)
