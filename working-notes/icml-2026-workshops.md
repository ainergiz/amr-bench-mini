# ICML 2026 — Tier-1 Workshop Submission Targets

**Compiled:** 2026-04-25
**Conference:** ICML 2026, Seoul, South Korea — workshops July 10–11, 2026
**Filter:** Workshops aligned with deployed AI agents, biomedical/life-sciences ML, and audio (clinical-trial patient recruitment & retention focus).

All six workshops are **non-archival** and **dual-submission friendly** — the same paper can be reframed and submitted to multiple venues.

---

## Deadline summary (sorted by urgency)

| # | Workshop | Deadline (AOE unless noted) | Page limit | Submission portal |
|---|---|---|---|---|
| 1 | **SD4H** — Structured Data for Health | **2026-04-28** | 4 pages | OpenReview |
| 2 | **GenBio** — Generative & Agentic AI for Biology | **2026-05-01** | 4 (short) / 9 (long) | OpenReview |
| 3 | **AIWILD** — Agents in the Wild: Safety, Security & Beyond | **2026-05-01** | 4 (short) / 9 (full) | OpenReview |
| 4 | **FM4LS** — Multi-modal FM/LLMs for Life Sciences | **2026-05-02 5:59 PM** (per OpenReview) | TBD | OpenReview |
| 5 | **FMAI** — Failure Modes in Agentic AI | **2026-05-08** (suggested early: 2026-04-24) | 8 pages | OpenReview |
| 6 | **ML4Audio** — Learning to Listen | **2026-05-23 23:59:59** | 4 pages | Microsoft CMT |

---

## 1. SD4H — Structured Data for Health 🚨 Most urgent

**Why for us:** Tabular EHR, irregular clinical measurements, biosignals — exactly the data we work with. Topics explicitly include *Deployment & Implementation: Real-world case studies and MLOps, federated evaluation, online learning during deployment.* The workshop explicitly welcomes deployed-agent / applied work.

- **Site:** https://structureddata4health.github.io
- **Call for Papers:** https://structureddata4health.github.io/call_for_papers.html
- **OpenReview:** https://openreview.net/group?id=ICML.cc/2026/Workshop/SD4H
- **Submission deadline:** 2026-04-28 AOE
- **Page limit:** 4 pages (excluding references and appendices)
- **Template:** Official ICML'26 author instructions; paper checklist NOT required
- **Anonymization:** Fully anonymized (double-blind)
- **Archival:** Non-archival
- **Dual submission:** Allowed (verify policies of any concurrent venue)
- **Preprints:** Allowed (arXiv etc.)
- **Presentation:** In-person required for accepted work
- **Contact:** sd4h.chairs@gmail.com

### Topics of interest
- Structured Adaptation: LLMs/methods to introduce structure to free-text
- Irregular & missing data
- Complex signals (high-dimensional / multi-resolution)
- Causal inference
- Representation learning & adaptation (across patients, devices, test-time)
- Clinical applications: forecasting, risk stratification, digital biomarkers
- Trust & reliability: explainability, fairness, robustness, privacy
- **Deployment & implementation: real-world case studies, MLOps, federated evaluation, online learning**
- New resources: datasets, benchmarks, software

### Possible angles for our team
- Patient-eligibility screening from semi-structured EHR — case study
- Online/test-time adaptation when site EHR schemas drift
- Fairness/robustness across recruitment-site populations
- Privacy-preserving evaluation across trial sites

---

## 2. GenBio — Generative & Agentic AI for Biology

**Why for us:** This workshop is the most direct ideological fit — it explicitly frames itself around the shift toward **agentic AI** in biology, and includes *human-AI collaboration paradigms* and *safety, governance, and ethical considerations*.

- **Site:** https://genbio-workshop.github.io/2026/
- **OpenReview:** https://openreview.net/group?id=ICML.cc/2026/Workshop/GenBio
- **LaTeX template (Overleaf):** https://www.overleaf.com/read/dnjfbdnypxwn#79923f
- **Submission deadline:** 2026-05-01 AOE (11:59 PM UTC-12)
- **Notification:** 2026-05-21
- **Camera-ready:** 2026-06-04
- **Page limit:** 4 pages (short) or 9 pages (long), excluding references and appendices
- **Anonymization:** Double-blind; OpenReview profile required at submission
- **Archival:** Non-archival
- **Contact:** genbio-icml2026-organizers@googlegroups.com

### Topics of interest
- Agent-based systems for hypothesis generation, experimental planning, closed-loop wet-lab integration
- Foundation/world models for multi-scale biology
- Benchmarks and evaluation frameworks for autonomous scientific systems
- Human-AI collaboration paradigms in biological research
- Safety, governance, ethical considerations of autonomous biological AI

### Possible angles for our team
- Agentic systems for trial design / cohort discovery as a "biological discovery" workflow
- Eval frameworks for closed-loop patient-recruitment agents
- Human-in-the-loop coordination patterns we've found necessary in production
- Safety/governance lessons from deploying agents in a regulated bio context

---

## 3. AIWILD — Agents in the Wild: Safety, Security, and Beyond

**Why for us:** Only ICML 2026 workshop with "in the wild" framing — explicitly built for production-deployed agents. Builds on ICLR 2026 first edition (235 submissions, ~800 attendees). The workshop has noted that "agentic AI" appeared in 60+ ICML workshop proposals, so this is the venue people will be reading.

- **Site:** https://agentwild-workshop.github.io/icml2026/
- **OpenReview:** https://openreview.net/group?id=ICML.cc/2026/Workshop/AIWILD
- **Template:** ICML 2026 LaTeX style + workshop-specific modified template (download `assets/icml_aiwild_template.zip` from site)
- **Submission deadline:** 2026-05-01 AOE
- **Notification:** 2026-05-15 AOE
- **Camera-ready:** 2026-06-15 AOE
- **Page limit:** 4 pages (short) or 9 pages (regular), excluding references/supplements
- **Anonymization:** Double-blind
- **Archival:** Non-archival; work under review or recently accepted elsewhere is welcome
- **Dual submission:** Permitted
- **Contact:** agentwild-workshop-icml2026@googlegroups.com

### Topics of interest
- Agentic safety & alignment
- Security, privacy, robustness (prompt injection, tool misuse, adversarial attacks on multi-agent coordination)
- Hallucination, interpretability, fairness
- Benchmarking
- Multimodal agents, multi-agent coordination
- Post-training
- Agent infrastructure
- Ethics & governance

### Possible angles for our team
- Prompt injection / jailbreak attempts seen by production patient-facing agents
- Privacy threats specific to clinical agents (PHI leakage via tool calls)
- Robustness benchmarks for healthcare agents in adversarial conditions
- Governance patterns we've adopted for HIPAA-context deployment

---

## 4. FM4LS — Multi-modal Foundation Models & LLMs for Life Sciences

**Why for us:** Established life-sciences venue (3rd edition); friendly to multi-modal work that integrates patient text + structured data + biosignals. LLM-agent topics for biomedical data are explicitly listed.

- **Site:** https://icml2026fm4ls.github.io
- **OpenReview:** https://openreview.net/group?id=ICML.cc/2026/Workshop/FM4LS
- **Submission start:** 2026-04-01 8:00 AM (per OpenReview venue)
- **Submission deadline:** 2026-05-02 5:59 PM (per OpenReview venue — confirm timezone on site)
- **Page limit / template / notification / camera-ready:** Not yet posted on workshop site (CFP page still being filled in). Past edition was 4 pages short / longer-paper option; expect similar.
- **Archival:** Past editions non-archival; assume same.
- **Contact:** icml2026fm4ls@gmail.com

### Topics of interest
- Multi-modal FMs for proteins, DNA, RNA, transcriptomic, metabolomic, etc.
- Multi-modal LLMs for biomolecular function prediction
- **LLM agents handling biomedical data**
- Multi-omics joint representation learning
- Generative models for biomolecule design
- Applications in drug discovery, precision medicine, personalized treatment
- Interpretability and robustness of bio-focused models

### Possible angles for our team
- LLM agents handling clinical/biomedical patient data (eligibility, EHR triage)
- Multi-modal patient-state representations (text + structured EHR + biosignals)
- Personalized-treatment / precision-medicine angle on retention

### TODO before submitting
- [ ] Email organizers (icml2026fm4ls@gmail.com) to confirm page limit, template, and notification dates
- [ ] Verify exact deadline timezone (5:59 PM is unusual — likely Pacific or UTC)

---

## 5. FMAI — Failure Modes in Agentic AI

**Why for us:** This workshop is *literally* asking for case studies of agent failures in deployment — reproducible triggers, trace diagnostics, verified fixes. We have production traces of failures at every level (tool calls, memory writes, recovery decisions). Strongest match for an applied/empirical paper.

- **Site:** https://fmai-workshop.github.io/
- **OpenReview:** https://openreview.net/group?id=ICML.cc/2026/Workshop/FMAI
- **Submission deadline:** 2026-05-08 AOE *(local: 2026-05-09 12:59 PM GMT+1)*
- **Suggested early submission:** 2026-04-24 AOE (already past)
- **Page limit:** 8 pages, excluding references and appendix
- **Template:** ICML format
- **Archival:** Non-archival; authors retain rights and can publish elsewhere
- **Dual submission:** Permitted
- **Best Paper Award:** Eligible
- **Contact:** fmaiworkshop@gmail.com

### What the workshop wants (four research outputs)
1. **Operational definitions** of agent failure modes
2. **Reproducible triggers** — minimal reproductions
3. **Comparable diagnostics** — closed-loop evaluation, trace diagnostics, counterfactual testing
4. **Verified fixes** — training/system interventions, mitigations, recovery, memory/tool-interface improvements

Plus: **well-documented negative results with transferable lessons.**

### Possible angles for our team
- Taxonomy of long-horizon failure modes seen in patient-recruitment agents
- Trace diagnostics framework for tool-call cascades in clinical workflows
- Documented negative results (what did *not* fix retention-agent drift)
- Memory/tool-interface improvements that demonstrably reduced specific failure classes

---

## 6. ML4Audio — Learning to Listen

**Why for us:** Only pure-audio workshop at ICML 2026. Relevant for any voice-agent component — TTS for outreach, ASR for screening calls, dialog modeling, voice-based eligibility flows. Modulate and Hume AI are contributing speech datasets.

- **Site:** https://mlforaudioworkshop.github.io/
- **Submission portal:** Microsoft CMT (link TBA on site — *not* OpenReview)
- **Submission deadline:** 2026-05-23 23:59:59 AOE
- **Notification:** 2026-06-09 AOE
- **Page limit:** Up to 4 pages, excluding references
- **Template:** ICML format
- **Archival:** Non-archival — accepted papers posted on workshop website only
- **Contact:** mlforaudioworkshop@gmail.com

### Topics of interest
- Speech modeling
- Environmental sound generation
- Novel generative models
- Music generation (raw audio)
- Text-to-speech methods
- Speech/music denoising
- Data augmentation
- Acoustic event classification, transcription, source separation
- Multimodal problems

### Possible angles for our team
- Robust ASR for clinical-screening calls (low-quality phone audio, accents, medical terminology)
- TTS calibration / voice design for patient outreach (trust, comprehension)
- Multimodal patient-call analysis (audio + transcript + structured outcome)
- Speech-based eligibility intake — accuracy under realistic conditions

---

## Strategic notes

1. **One paper, multiple venues.** All six are non-archival with dual submission allowed. A single piece of work can be reframed:
   - Failure-modes framing → FMAI
   - Safety/security framing → AIWILD
   - Bio/scientific framing → GenBio
   - Clinical-data framing → SD4H
   - Multi-modal life-science framing → FM4LS
   - Audio framing → ML4Audio

2. **Highest-leverage candidates given our position:**
   - **SD4H** + **FMAI**: applied / case-study writeups using the trial-recruitment data and failure traces we already have.
   - **AIWILD**: safety/security writeup of attacks/defenses on production agents.
   - **GenBio**: requires more bio-discovery framing — strongest fit if we have eval-framework or human-AI collaboration work.

3. **Per-workshop next actions:**
   - SD4H (4 days): scope a 4-page paper *now* if we have anything close.
   - GenBio + AIWILD (1 week): main agent-safety / agentic-bio paper.
   - FM4LS (1 week): confirm CFP details with organizers.
   - FMAI (~2 weeks): full failure-modes paper, 8 pages — most room to develop.
   - ML4Audio (~4 weeks): audio-component spinoff if we have voice-agent eval data.

---

## Source links

- [ICML 2026 workshops announcement](https://blog.icml.cc/2026/04/06/announcing-the-icml-2026-workshops-and-affinity-workshops/)
- [ICML 2026 Workshop OpenReview group](https://openreview.net/group?id=ICML.cc/2026/Workshop)
