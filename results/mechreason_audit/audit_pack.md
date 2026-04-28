# MechReason Label Audit — stratified sample

This pack contains 29 MechReason cases sampled across mechanism classes (weighted toward `permeability_loss`, `regulator_loss_of_function`, and `insufficient_evidence` — the categories most likely to be miscalled by the heuristic). Each card shows the task input as the agent sees it, plus the heuristic-derived gold for auditor review.

Mark decisions in `audit_form.tsv` (one row per task here). Valid mechanism classes: `efflux, enzymatic_inactivation, insufficient_evidence, intrinsic, metabolic_bypass, permeability_loss, regulator_loss_of_function, target_modification, target_protection`.

---

## 1. mechreason_kp_000162  ·  `efflux`

- **Genome**: Klebsiella pneumoniae KPN295ec (573.14032)
- **Metadata**: collection_year: 2012 · contigs: 106 · gc_content: 57.2 · genome_length: 5575528 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `tetracycline` (class: tetracycline)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `ramR_E113PfsTer7` | MULTIDRUG / CHLORAMPHENICOL/FLUOROQUINOLONE/TEMOCILLIN/TETRACYCLINE/TIGECYCLINE | 99.5% / 100.0% | POINTX |
| AMRFinderPlus | `tet(A)` | TETRACYCLINE / TETRACYCLINE | 100.0% / 100.0% | EXACTX |
| ResFinder | `tet(A)` | Doxycycline, Tetracycline | 100.0% / 100.0% |  |

**Heuristic gold:** `efflux` · required_genes=['teta']

> _Heuristic rationale:_ Direct tetracycline-specific MFS efflux pump (tet) confers tetracycline R; any regulator LoF is supplementary.

_Coverage context: agent saw 3 drug-relevant hits; the underlying isolate has 20 total AMRFinder + 13 total ResFinder hits._

---

## 2. mechreason_kp_000233  ·  `efflux`

- **Genome**: Klebsiella pneumoniae KPN956ec (573.14522)
- **Metadata**: collection_year: 2013 · contigs: 65 · gc_content: 57.31 · genome_length: 5416011 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `nitrofurantoin` (class: nitrofuran)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `nfsB_K130QfsTer5` | NITROFURAN / NITROFURANTOIN | 99.5% / 100.0% | POINTX |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |

**Heuristic gold:** `efflux` · required_genes=['oqxa']

> _Heuristic rationale:_ Active efflux pumps reduce intracellular drug accumulation.

_Coverage context: agent saw 2 drug-relevant hits; the underlying isolate has 12 total AMRFinder + 8 total ResFinder hits._

---

## 3. mechreason_kp_000273  ·  `efflux`

- **Genome**: Klebsiella pneumoniae strain INF074 (573.15520)
- **Metadata**: contigs: 67 · gc_content: 57.28 · genome_length: 5405294 · host_name: Human, Homo sapiens · isolation_country: Australia · mlst: MLST.klebsiella.111
- **Antibiotic**: `nitrofurantoin` (class: nitrofuran)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |

**Heuristic gold:** `efflux` · required_genes=['oqxa']

> _Heuristic rationale:_ Active efflux pumps reduce intracellular drug accumulation.

_Coverage context: agent saw 1 drug-relevant hits; the underlying isolate has 4 total AMRFinder + 8 total ResFinder hits._

---

## 4. mechreason_kp_000224  ·  `enzymatic_inactivation`

- **Genome**: Klebsiella pneumoniae KPN956ec (573.14522)
- **Metadata**: collection_year: 2013 · contigs: 65 · gc_content: 57.31 · genome_length: 5416011 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `aztreonam` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaCTX-M` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 99.0% | BLASTX |
| AMRFinderPlus | `blaSHV-28` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaTEM-1` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `ompK35_G208VfsTer5` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | POINTX |
| ResFinder | `blaCTX-M-15` | Amoxicillin, Ampicillin, Aztreonam, Cefepime, Cefotaxime, Ceftazidime, Ceftriaxo | 100.0% / 99.0% |  |
| ResFinder | `blaSHV-106` | Amoxicillin, Ampicillin, Aztreonam, Cefepime, Cefotaxime, Ceftazidime, Ceftriaxo | 99.9% / 100.0% |  |
| ResFinder | `blaSHV-28` | Unknown Beta-lactam | 99.9% / 100.0% |  |

**Heuristic gold:** `enzymatic_inactivation` · required_genes=['blactxm', 'blactxm15', 'blashv106', 'blashv28', 'blatem1']

> _Heuristic rationale:_ β-lactamase hydrolyzes the β-lactam ring; phenotype depends on enzyme class and porin status.

_Coverage context: agent saw 7 drug-relevant hits; the underlying isolate has 12 total AMRFinder + 8 total ResFinder hits._

---

## 5. mechreason_kp_000439  ·  `enzymatic_inactivation`

- **Genome**: Klebsiella pneumoniae strain 18 (573.24256)
- **Metadata**: collection_year: 2013 · contigs: 89 · gc_content: 57.310154 · genome_length: 5472189 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `ampicillin` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaCTX-M-15` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaOXA-1` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaOXA-232` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaSHV-28` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `ompK36_D135DGD` | BETA-LACTAM / CARBAPENEM | 94.9% / 100.0% | POINTX |
| ResFinder | `blaCTX-M-15` | Amoxicillin, Ampicillin, Aztreonam, Cefepime, Cefotaxime, Ceftazidime, Ceftriaxo | 100.0% / 100.0% |  |
| ResFinder | `blaOXA-1` | Amoxicillin, Amoxicillin+Clavulanic acid, Ampicillin, Ampicillin+Clavulanic acid | 100.0% / 100.0% |  |
| ResFinder | `blaOXA-232` | Amoxicillin, Amoxicillin+Clavulanic acid, Ampicillin, Ampicillin+Clavulanic acid | 100.0% / 100.0% |  |
| ResFinder | `blaSHV-106` | Amoxicillin, Ampicillin, Aztreonam, Cefepime, Cefotaxime, Ceftazidime, Ceftriaxo | 99.9% / 100.0% |  |
| ResFinder | `blaSHV-28` | Unknown Beta-lactam | 99.9% / 100.0% |  |

**Heuristic gold:** `enzymatic_inactivation` · required_genes=['blactxm15', 'blaoxa1', 'blaoxa232', 'blashv106', 'blashv28']

> _Heuristic rationale:_ β-lactamase hydrolyzes the β-lactam ring; phenotype depends on enzyme class and porin status.

_Coverage context: agent saw 10 drug-relevant hits; the underlying isolate has 15 total AMRFinder + 12 total ResFinder hits._

---

## 6. mechreason_kp_000698  ·  `enzymatic_inactivation`

- **Genome**: Klebsiella pneumoniae strain MUGSI_309 (573.24391)
- **Metadata**: collection_year: 2014 · contigs: 186 · gc_content: 57.08151 · genome_length: 5668380 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `meropenem` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaKPC-3` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaSHV-11` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| ResFinder | `blaKPC-3` | Amoxicillin, Amoxicillin+Clavulanic acid, Ampicillin, Ampicillin+Clavulanic acid | 100.0% / 100.0% |  |
| ResFinder | `blaSHV-158` | Unknown Beta-lactam | 99.9% / 100.0% |  |
| ResFinder | `blaSHV-159` | Unknown Beta-lactam | 99.9% / 100.0% |  |
| ResFinder | `blaSHV-182` | Unknown Beta-lactam | 99.9% / 100.0% |  |

**Heuristic gold:** `enzymatic_inactivation` · required_genes=['blakpc3', 'blashv11', 'blashv158', 'blashv159', 'blashv182']

> _Heuristic rationale:_ β-lactamase hydrolyzes the β-lactam ring; phenotype depends on enzyme class and porin status.

_Coverage context: agent saw 6 drug-relevant hits; the underlying isolate has 21 total AMRFinder + 19 total ResFinder hits._

---

## 7. mechreason_kp_000881  ·  `enzymatic_inactivation`

- **Genome**: Klebsiella pneumoniae strain W2-13-ERG11 (573.5722)
- **Metadata**: collection_year: 2015 · contigs: 46 · gc_content: 57.36 · genome_length: 5493144 · isolation_country: Thailand · mlst: MLST.klebsiella.895
- **Antibiotic**: `cefuroxime` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaCTX-M-27` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaDHA-1` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaSHV-11` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| ResFinder | `blaSHV-158` | Unknown Beta-lactam | 99.9% / 100.0% |  |
| ResFinder | `blaSHV-159` | Unknown Beta-lactam | 99.9% / 100.0% |  |
| ResFinder | `blaSHV-182` | Unknown Beta-lactam | 99.9% / 100.0% |  |

**Heuristic gold:** `enzymatic_inactivation` · required_genes=['blactxm27', 'bladha1', 'blashv11', 'blashv158', 'blashv159', 'blashv182']

> _Heuristic rationale:_ β-lactamase hydrolyzes the β-lactam ring; phenotype depends on enzyme class and porin status.

_Coverage context: agent saw 6 drug-relevant hits; the underlying isolate has 20 total AMRFinder + 19 total ResFinder hits._

---

## 8. mechreason_kp_000103  ·  `insufficient_evidence`

- **Genome**: Klebsiella pneumoniae KPN1543ec (573.13472)
- **Metadata**: collection_year: 2014 · contigs: 75 · gc_content: 57.3 · genome_length: 5482466 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `ciprofloxacin` (class: quinolone)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `aac(6')-Ib-cr5` | AMINOGLYCOSIDE/QUINOLONE / AMIKACIN/KANAMYCIN/QUINOLONE/TOBRAMYCIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB19` | PHENICOL/QUINOLONE / PHENICOL/QUINOLONE | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `qnrB1` | QUINOLONE / QUINOLONE | 100.0% / 100.0% | ALLELEX |
| ResFinder | `OqxA` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 99.9% / 100.0% |  |
| ResFinder | `OqxB` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 99.0% / 100.0% |  |
| ResFinder | `aac(6')-Ib-cr` | Tobramycin, Dibekacin, Amikacin, Sisomicin, Netilmicin, Fluoroquinolone, Ciprofl | 100.0% / 100.0% |  |
| ResFinder | `qnrB1` | Ciprofloxacin | 100.0% / 100.0% |  |

**Heuristic gold:** `insufficient_evidence` · required_genes=[]

> _Heuristic rationale:_ Visible annotator evidence does not deterministically map to a mechanism for this drug; HypothesisGen flavor.

_Coverage context: agent saw 8 drug-relevant hits; the underlying isolate has 16 total AMRFinder + 18 total ResFinder hits._

---

## 9. mechreason_kp_000281  ·  `insufficient_evidence`

- **Genome**: Klebsiella pneumoniae strain KSB1_6J (573.15595)
- **Metadata**: contigs: 75 · gc_content: 57.35 · genome_length: 5445588 · host_name: Human, Homo sapiens · isolation_country: Australia · mlst: MLST.klebsiella.323
- **Antibiotic**: `ciprofloxacin` (class: quinolone)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `aac(6')-Ib-cr5` | AMINOGLYCOSIDE/QUINOLONE / AMIKACIN/KANAMYCIN/QUINOLONE/TOBRAMYCIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB19` | PHENICOL/QUINOLONE / PHENICOL/QUINOLONE | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `qnrB1` | QUINOLONE / QUINOLONE | 100.0% / 100.0% | ALLELEX |
| ResFinder | `OqxA` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 99.5% / 100.0% |  |
| ResFinder | `OqxB` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 98.8% / 100.0% |  |
| ResFinder | `aac(6')-Ib-cr` | Tobramycin, Dibekacin, Amikacin, Sisomicin, Netilmicin, Fluoroquinolone, Ciprofl | 100.0% / 100.0% |  |
| ResFinder | `qnrB1` | Ciprofloxacin | 100.0% / 100.0% |  |

**Heuristic gold:** `insufficient_evidence` · required_genes=[]

> _Heuristic rationale:_ Visible annotator evidence does not deterministically map to a mechanism for this drug; HypothesisGen flavor.

_Coverage context: agent saw 8 drug-relevant hits; the underlying isolate has 16 total AMRFinder + 17 total ResFinder hits._

---

## 10. mechreason_kp_000342  ·  `insufficient_evidence`

- **Genome**: Klebsiella pneumoniae strain CCUG 70742 (573.18476)
- **Metadata**: collection_year: 2012 · contigs: 5 · gc_content: 57.40553 · genome_length: 5391141 · host_name: Human, Homo sapiens · isolation_country: Sweden
- **Antibiotic**: `tigecycline` (class: tetracycline)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 99.8% / 100.0% | BLASTX |
| AMRFinderPlus | `tet(A)` | TETRACYCLINE / TETRACYCLINE | 100.0% / 100.0% | EXACTX |
| ResFinder | `tet(A)` | Doxycycline, Tetracycline | 100.0% / 100.0% |  |

**Heuristic gold:** `insufficient_evidence` · required_genes=[]

> _Heuristic rationale:_ Wild-type tet(A) and oqxAB cannot drive tigecycline R; no regulator LoF (ramR/acrR/oqxR/marR) nor tigecycline-active tet variant detected. HypothesisGen flavor.

_Coverage context: agent saw 4 drug-relevant hits; the underlying isolate has 17 total AMRFinder + 17 total ResFinder hits._

---

## 11. mechreason_kp_000532  ·  `insufficient_evidence`

- **Genome**: Klebsiella pneumoniae strain MRSN19181 (573.24323)
- **Metadata**: collection_year: 2013 · contigs: 141 · gc_content: 56.8855 · genome_length: 5807116 · host_name: Human, Homo sapiens · isolation_country: Honduras
- **Antibiotic**: `tigecycline` (class: tetracycline)
- **AST phenotype**: `Intermediate`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `tet(A)` | TETRACYCLINE / TETRACYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `tet(G)` | TETRACYCLINE / TETRACYCLINE | 100.0% / 100.0% | EXACTX |
| ResFinder | `tet(A)` | Doxycycline, Tetracycline | 100.0% / 100.0% |  |
| ResFinder | `tet(G)` | Doxycycline, Tetracycline | 100.0% / 100.0% |  |

**Heuristic gold:** `insufficient_evidence` · required_genes=[]

> _Heuristic rationale:_ Wild-type tet(A) and oqxAB cannot drive tigecycline R; no regulator LoF (ramR/acrR/oqxR/marR) nor tigecycline-active tet variant detected. HypothesisGen flavor.

_Coverage context: agent saw 5 drug-relevant hits; the underlying isolate has 29 total AMRFinder + 50 total ResFinder hits._

---

## 12. mechreason_kp_000565  ·  `insufficient_evidence`

- **Genome**: Klebsiella pneumoniae strain MUGSI_133 (573.24349)
- **Metadata**: collection_year: 2014 · contigs: 135 · gc_content: 57.220993 · genome_length: 5594948 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `levofloxacin` (class: quinolone)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `aac(6')-Ib-cr5` | AMINOGLYCOSIDE/QUINOLONE / AMIKACIN/KANAMYCIN/QUINOLONE/TOBRAMYCIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `oqxA11` | PHENICOL/QUINOLONE / PHENICOL/QUINOLONE | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `oqxB19` | PHENICOL/QUINOLONE / PHENICOL/QUINOLONE | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `qnrB1` | QUINOLONE / QUINOLONE | 100.0% / 100.0% | ALLELEX |
| ResFinder | `aac(6')-Ib-cr` | Tobramycin, Dibekacin, Amikacin, Sisomicin, Netilmicin, Fluoroquinolone, Ciprofl | 100.0% / 100.0% |  |

**Heuristic gold:** `insufficient_evidence` · required_genes=[]

> _Heuristic rationale:_ Visible annotator evidence does not deterministically map to a mechanism for this drug; HypothesisGen flavor.

_Coverage context: agent saw 5 drug-relevant hits; the underlying isolate has 15 total AMRFinder + 22 total ResFinder hits._

---

## 13. mechreason_kp_000870  ·  `insufficient_evidence`

- **Genome**: Klebsiella pneumoniae strain 5_GR_13 (573.5644)
- **Metadata**: collection_year: 2013 · contigs: 138 · gc_content: 56.77 · genome_length: 5889874 · host_name: Human, Homo sapiens · isolation_country: Greece
- **Antibiotic**: `polymyxin b` (class: polymyxin)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

*(no relevant tool hits for this drug — HypothesisGen flavor)*

**Heuristic gold:** `insufficient_evidence` · required_genes=[]

> _Heuristic rationale:_ Visible annotator evidence does not deterministically map to a mechanism for this drug; HypothesisGen flavor.

_Coverage context: agent saw 0 drug-relevant hits; the underlying isolate has 31 total AMRFinder + 32 total ResFinder hits._

---

## 14. mechreason_kp_000896  ·  `intrinsic`

- **Genome**: Klebsiella pneumoniae strain 22_GR_12 (573.5765)
- **Metadata**: collection_year: 2012 · contigs: 105 · gc_content: 57.01 · genome_length: 5750411 · host_name: Human, Homo sapiens · isolation_country: Greece
- **Antibiotic**: `fosfomycin` (class: fosfomycin)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `fosA` | FOSFOMYCIN / FOSFOMYCIN | 98.6% / 100.0% | BLASTX |
| ResFinder | `fosA6` | Fosfomycin | 98.8% / 100.0% |  |

**Heuristic gold:** `intrinsic` · required_genes=['fosa', 'fosa6']

> _Heuristic rationale:_ Klebsiella encodes a chromosomal fosA-family glutathione transferase; intrinsic elevation of fosfomycin MIC.

_Coverage context: agent saw 2 drug-relevant hits; the underlying isolate has 17 total AMRFinder + 18 total ResFinder hits._

---

## 15. mechreason_kp_000395  ·  `metabolic_bypass`

- **Genome**: Klebsiella pneumoniae strain 10 (573.24243)
- **Metadata**: collection_year: 2012 · contigs: 164 · gc_content: 56.76292 · genome_length: 5817498 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `trimethoprim/sulfamethoxazole` (class: folate pathway antagonist)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `dfrA1` | TRIMETHOPRIM / TRIMETHOPRIM | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `dfrA12` | TRIMETHOPRIM / TRIMETHOPRIM | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `sul1` | SULFONAMIDE / SULFONAMIDE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `sul2` | SULFONAMIDE / SULFONAMIDE | 100.0% / 100.0% | EXACTX |
| ResFinder | `OqxA` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 99.2% / 100.0% |  |
| ResFinder | `OqxB` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 98.8% / 100.0% |  |
| ResFinder | `dfrA1` | Trimethoprim | 100.0% / 100.0% |  |
| ResFinder | `dfrA12` | Trimethoprim | 100.0% / 100.0% |  |
| ResFinder | `sul1` | Sulfamethoxazole | 100.0% / 100.0% |  |
| ResFinder | `sul2` | Sulfamethoxazole | 100.0% / 100.0% |  |

**Heuristic gold:** `metabolic_bypass` · required_genes=['dfra1', 'dfra12', 'sul1', 'sul2']

> _Heuristic rationale:_ Acquired drug-insensitive DHFR (dfr) and/or DHPS (sul) bypass the inhibited folate-pathway enzyme.

_Coverage context: agent saw 10 drug-relevant hits; the underlying isolate has 32 total AMRFinder + 33 total ResFinder hits._

---

## 16. mechreason_kp_000571  ·  `metabolic_bypass`

- **Genome**: Klebsiella pneumoniae strain MUGSI_133 (573.24349)
- **Metadata**: collection_year: 2014 · contigs: 135 · gc_content: 57.220993 · genome_length: 5594948 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `trimethoprim/sulfamethoxazole` (class: folate pathway antagonist)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `dfrA14` | TRIMETHOPRIM / TRIMETHOPRIM | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `sul2` | SULFONAMIDE / SULFONAMIDE | 100.0% / 100.0% | EXACTX |
| ResFinder | `OqxA` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 99.2% / 100.0% |  |
| ResFinder | `OqxB` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 98.6% / 100.0% |  |
| ResFinder | `dfrA14` | Trimethoprim | 100.0% / 100.0% |  |
| ResFinder | `sul2` | Sulfamethoxazole | 100.0% / 100.0% |  |

**Heuristic gold:** `metabolic_bypass` · required_genes=['dfra14', 'sul2']

> _Heuristic rationale:_ Acquired drug-insensitive DHFR (dfr) and/or DHPS (sul) bypass the inhibited folate-pathway enzyme.

_Coverage context: agent saw 6 drug-relevant hits; the underlying isolate has 15 total AMRFinder + 22 total ResFinder hits._

---

## 17. mechreason_kp_000760  ·  `metabolic_bypass`

- **Genome**: Klebsiella pneumoniae strain MUGSI_45 (573.24413)
- **Metadata**: collection_year: 2013 · contigs: 124 · gc_content: 57.28872 · genome_length: 5560286 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `trimethoprim/sulfamethoxazole` (class: folate pathway antagonist)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `dfrA12` | TRIMETHOPRIM / TRIMETHOPRIM | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `sul1` | SULFONAMIDE / SULFONAMIDE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `sul3` | SULFONAMIDE / SULFONAMIDE | 100.0% / 100.0% | EXACTX |
| ResFinder | `OqxA` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 100.0% / 100.0% |  |
| ResFinder | `OqxB` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 100.0% / 100.0% |  |
| ResFinder | `dfrA12` | Trimethoprim | 100.0% / 100.0% |  |
| ResFinder | `sul1` | Sulfamethoxazole | 100.0% / 100.0% |  |
| ResFinder | `sul3` | Sulfamethoxazole | 100.0% / 100.0% |  |

**Heuristic gold:** `metabolic_bypass` · required_genes=['dfra12', 'sul1', 'sul3']

> _Heuristic rationale:_ Acquired drug-insensitive DHFR (dfr) and/or DHPS (sul) bypass the inhibited folate-pathway enzyme.

_Coverage context: agent saw 8 drug-relevant hits; the underlying isolate has 23 total AMRFinder + 22 total ResFinder hits._

---

## 18. mechreason_kp_000408  ·  `permeability_loss`

- **Genome**: Klebsiella pneumoniae strain 104 (573.24245)
- **Metadata**: collection_year: 2015 · contigs: 82 · gc_content: 57.34934 · genome_length: 5393701 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `ertapenem` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaCTX-M` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 92.8% | BLASTX |
| AMRFinderPlus | `blaOXA-1` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaSHV-28` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaTEM-1` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `ompK36_G108LfsTer9` | BETA-LACTAM / CARBAPENEM | 92.7% / 100.0% | POINTX |
| ResFinder | `blaSHV-28` | Unknown Beta-lactam | 99.9% / 100.0% |  |

**Heuristic gold:** `permeability_loss` · required_genes=['ompk36g108lfster9']

> _Heuristic rationale:_ Porin loss in OmpK35/OmpK36 reduces periplasmic carbapenem accumulation; no carbapenemase detected so this is the dominant mechanism.

_Coverage context: agent saw 6 drug-relevant hits; the underlying isolate has 18 total AMRFinder + 20 total ResFinder hits._

---

## 19. mechreason_kp_000464  ·  `permeability_loss`

- **Genome**: Klebsiella pneumoniae strain 24 (573.24267)
- **Metadata**: collection_year: 2015 · contigs: 212 · gc_content: 57.1251 · genome_length: 5591171 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `cefoxitin` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaOXA` | BETA-LACTAM / BETA-LACTAM | 99.6% / 100.0% | INTERNAL_STOP |
| AMRFinderPlus | `blaSHV` | BETA-LACTAM / BETA-LACTAM | 100.0% / 91.6% | BLASTX |
| AMRFinderPlus | `blaTEM-1` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `ompK35_E42RfsTer47` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | POINTX |

**Heuristic gold:** `permeability_loss` · required_genes=['ompk35e42rfster47']

> _Heuristic rationale:_ Cefoxitin R driven by porin loss; non-AmpC β-lactamases (CTX-M, narrow SHV/TEM, OXA-1) cannot hydrolyze cefoxitin and are confounders here.

_Coverage context: agent saw 4 drug-relevant hits; the underlying isolate has 13 total AMRFinder + 12 total ResFinder hits._

---

## 20. mechreason_kp_000658  ·  `permeability_loss`

- **Genome**: Klebsiella pneumoniae strain MUGSI_225 (573.24380)
- **Metadata**: collection_year: 2014 · contigs: 119 · gc_content: 57.157852 · genome_length: 5647819 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `cefoxitin` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaSHV-11` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaTEM` | BETA-LACTAM / BETA-LACTAM | 100.0% / 52.5% | PARTIALX |
| AMRFinderPlus | `ompK35_E42RfsTer47` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | POINTX |
| ResFinder | `blaSHV-185` | Unknown Beta-lactam | 99.8% / 100.0% |  |
| ResFinder | `blaSHV-69` | Unknown Beta-lactam | 99.8% / 100.0% |  |

**Heuristic gold:** `permeability_loss` · required_genes=['ompk35e42rfster47']

> _Heuristic rationale:_ Cefoxitin R driven by porin loss; non-AmpC β-lactamases (CTX-M, narrow SHV/TEM, OXA-1) cannot hydrolyze cefoxitin and are confounders here.

_Coverage context: agent saw 5 drug-relevant hits; the underlying isolate has 17 total AMRFinder + 17 total ResFinder hits._

---

## 21. mechreason_kp_000715  ·  `permeability_loss`

- **Genome**: Klebsiella pneumoniae strain MUGSI_38 (573.24407)
- **Metadata**: collection_year: 2013 · contigs: 126 · gc_content: 57.300426 · genome_length: 5328168 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `imipenem` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaSHV-5` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaSHV_C-112A` | BETA-LACTAM / CEFIDEROCOL/CEPHALOSPORIN | 99.3% / 100.0% | POINTN |
| AMRFinderPlus | `blaTEM` | BETA-LACTAM / BETA-LACTAM | 100.0% / 94.8% | BLASTX |
| AMRFinderPlus | `ompK35_E42RfsTer47` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | POINTX |
| AMRFinderPlus | `ompK36_Q262PfsTer55` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | POINTX |

**Heuristic gold:** `permeability_loss` · required_genes=['ompk35e42rfster47', 'ompk36q262pfster55']

> _Heuristic rationale:_ Porin loss in OmpK35/OmpK36 reduces periplasmic carbapenem accumulation; no carbapenemase detected so this is the dominant mechanism.

_Coverage context: agent saw 5 drug-relevant hits; the underlying isolate has 16 total AMRFinder + 10 total ResFinder hits._

---

## 22. mechreason_kp_000731  ·  `permeability_loss`

- **Genome**: Klebsiella pneumoniae strain MUGSI_42 (573.24411)
- **Metadata**: collection_year: 2013 · contigs: 134 · gc_content: 56.931686 · genome_length: 5599098 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `doripenem` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaCTX-M-15` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaOXA-1` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaSHV-11` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaTEM-1` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `ompK35_G208VfsTer5` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | POINTX |
| ResFinder | `blaSHV-67` | Unknown Beta-lactam | 99.8% / 100.0% |  |

**Heuristic gold:** `permeability_loss` · required_genes=['ompk35g208vfster5']

> _Heuristic rationale:_ Porin loss in OmpK35/OmpK36 reduces periplasmic carbapenem accumulation; no carbapenemase detected so this is the dominant mechanism.

_Coverage context: agent saw 6 drug-relevant hits; the underlying isolate has 25 total AMRFinder + 24 total ResFinder hits._

---

## 23. mechreason_kp_000732  ·  `permeability_loss`

- **Genome**: Klebsiella pneumoniae strain MUGSI_42 (573.24411)
- **Metadata**: collection_year: 2013 · contigs: 134 · gc_content: 56.931686 · genome_length: 5599098 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `ertapenem` (class: beta-lactam)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `blaCTX-M-15` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaOXA-1` | BETA-LACTAM / CEPHALOSPORIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaSHV-11` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `blaTEM-1` | BETA-LACTAM / BETA-LACTAM | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `ompK35_G208VfsTer5` | BETA-LACTAM / CARBAPENEM | 100.0% / 100.0% | POINTX |
| ResFinder | `blaSHV-67` | Unknown Beta-lactam | 99.8% / 100.0% |  |

**Heuristic gold:** `permeability_loss` · required_genes=['ompk35g208vfster5']

> _Heuristic rationale:_ Porin loss in OmpK35/OmpK36 reduces periplasmic carbapenem accumulation; no carbapenemase detected so this is the dominant mechanism.

_Coverage context: agent saw 6 drug-relevant hits; the underlying isolate has 25 total AMRFinder + 24 total ResFinder hits._

---

## 24. mechreason_kp_000662  ·  `regulator_loss_of_function`

- **Genome**: Klebsiella pneumoniae strain MUGSI_225 (573.24380)
- **Metadata**: collection_year: 2014 · contigs: 119 · gc_content: 57.157852 · genome_length: 5647819 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `tetracycline` (class: tetracycline)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `ramR_E102SfsTer17` | MULTIDRUG / CHLORAMPHENICOL/FLUOROQUINOLONE/TEMOCILLIN/TETRACYCLINE/TIGECYCLINE | 100.0% / 100.0% | POINTX |

**Heuristic gold:** `regulator_loss_of_function` · required_genes=['ramre102sfster17']

> _Heuristic rationale:_ Loss-of-function in efflux regulator(s) derepresses AcrAB-TolC; no direct tet-specific efflux pump present.

_Coverage context: agent saw 3 drug-relevant hits; the underlying isolate has 17 total AMRFinder + 17 total ResFinder hits._

---

## 25. mechreason_kp_000922  ·  `regulator_loss_of_function`

- **Genome**: Klebsiella pneumoniae strain AR_0049 (573.7362)
- **Metadata**: contigs: 4 · gc_content: 56.97 · genome_length: 5779484 · mlst: MLST.klebsiella.11 · sequencing_status: Complete · strain: AR_0049
- **Antibiotic**: `tigecycline` (class: tetracycline)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `ramR_Y59CfsTer13` | MULTIDRUG / CHLORAMPHENICOL/FLUOROQUINOLONE/TEMOCILLIN/TETRACYCLINE/TIGECYCLINE | 100.0% / 100.0% | POINTX |
| AMRFinderPlus | `tet(A)` | TETRACYCLINE / TETRACYCLINE | 100.0% / 100.0% | EXACTX |
| ResFinder | `tet(A)` | Doxycycline, Tetracycline | 100.0% / 100.0% |  |

**Heuristic gold:** `regulator_loss_of_function` · required_genes=['ramry59cfster13']

> _Heuristic rationale:_ Loss-of-function in efflux regulator(s) derepresses AcrAB-TolC and related pumps; modal tigecycline-R mechanism in K. pneumoniae.

_Coverage context: agent saw 5 drug-relevant hits; the underlying isolate has 30 total AMRFinder + 34 total ResFinder hits._

---

## 26. mechreason_kp_000337  ·  `target_modification`

- **Genome**: Klebsiella pneumoniae strain CCUG 70742 (573.18476)
- **Metadata**: collection_year: 2012 · contigs: 5 · gc_content: 57.40553 · genome_length: 5391141 · host_name: Human, Homo sapiens · isolation_country: Sweden
- **Antibiotic**: `ciprofloxacin` (class: quinolone)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `aac(6')-Ib-cr5` | AMINOGLYCOSIDE/QUINOLONE / AMIKACIN/KANAMYCIN/QUINOLONE/TOBRAMYCIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `gyrA_S83I` | QUINOLONE / QUINOLONE | 99.8% / 100.0% | POINTX |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 99.8% / 100.0% | BLASTX |
| AMRFinderPlus | `parC_S80I` | QUINOLONE / QUINOLONE | 99.3% / 98.8% | POINTX |
| ResFinder | `OqxA` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 99.5% / 100.0% |  |
| ResFinder | `OqxB` | Chloramphenicol, Nalidixic acid, Ciprofloxacin, Trimethoprim | 98.5% / 100.0% |  |
| ResFinder | `aac(6')-Ib-cr` | Tobramycin, Dibekacin, Amikacin, Sisomicin, Netilmicin, Fluoroquinolone, Ciprofl | 100.0% / 100.0% |  |

**Heuristic gold:** `target_modification` · required_genes=['gyras83i', 'parcs80i']

> _Heuristic rationale:_ QRDR mutation in gyrase or topoisomerase IV target reduces fluoroquinolone binding.

_Coverage context: agent saw 8 drug-relevant hits; the underlying isolate has 17 total AMRFinder + 17 total ResFinder hits._

---

## 27. mechreason_kp_000391  ·  `target_modification`

- **Genome**: Klebsiella pneumoniae strain 10 (573.24243)
- **Metadata**: collection_year: 2012 · contigs: 164 · gc_content: 56.76292 · genome_length: 5817498 · host_name: Human, Homo sapiens · isolation_country: USA
- **Antibiotic**: `levofloxacin` (class: quinolone)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `gyrA_D87G` | QUINOLONE / QUINOLONE | 99.5% / 100.0% | POINTX |
| AMRFinderPlus | `gyrA_S83Y` | QUINOLONE / QUINOLONE | 99.5% / 100.0% | POINTX |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 99.9% / 100.0% | BLASTX |
| AMRFinderPlus | `parC_S80I` | QUINOLONE / QUINOLONE | 99.4% / 98.8% | POINTX |

**Heuristic gold:** `target_modification` · required_genes=['gyrad87g', 'gyras83y', 'parcs80i']

> _Heuristic rationale:_ QRDR mutation in gyrase or topoisomerase IV target reduces fluoroquinolone binding.

_Coverage context: agent saw 5 drug-relevant hits; the underlying isolate has 32 total AMRFinder + 33 total ResFinder hits._

---

## 28. mechreason_kp_000528  ·  `target_modification`

- **Genome**: Klebsiella pneumoniae strain MRSN19181 (573.24323)
- **Metadata**: collection_year: 2013 · contigs: 141 · gc_content: 56.8855 · genome_length: 5807116 · host_name: Human, Homo sapiens · isolation_country: Honduras
- **Antibiotic**: `moxifloxacin` (class: quinolone)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `aac(6')-Ib-cr5` | AMINOGLYCOSIDE/QUINOLONE / AMIKACIN/KANAMYCIN/QUINOLONE/TOBRAMYCIN | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `gyrA_D87N` | QUINOLONE / QUINOLONE | 99.5% / 100.0% | POINTX |
| AMRFinderPlus | `gyrA_S83F` | QUINOLONE / QUINOLONE | 99.5% / 100.0% | POINTX |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB32` | PHENICOL/QUINOLONE / PHENICOL/QUINOLONE | 100.0% / 100.0% | ALLELEX |
| AMRFinderPlus | `parC_E84K` | QUINOLONE / QUINOLONE | 99.3% / 98.8% | POINTX |
| ResFinder | `aac(6')-Ib-cr` | Tobramycin, Dibekacin, Amikacin, Sisomicin, Netilmicin, Fluoroquinolone, Ciprofl | 100.0% / 100.0% |  |

**Heuristic gold:** `target_modification` · required_genes=['gyrad87n', 'gyras83f', 'parce84k']

> _Heuristic rationale:_ QRDR mutation in gyrase or topoisomerase IV target reduces fluoroquinolone binding.

_Coverage context: agent saw 7 drug-relevant hits; the underlying isolate has 29 total AMRFinder + 50 total ResFinder hits._

---

## 29. mechreason_kp_000838  ·  `target_modification`

- **Genome**: Klebsiella pneumoniae KP-42LI (573.46864)
- **Metadata**: contigs: 99 · gc_content: 56.550926 · genome_length: 5875704 · host_name: Human, Homo sapiens · isolation_country: Italy · mlst: MLST.klebsiella.147
- **Antibiotic**: `levofloxacin` (class: quinolone)
- **AST phenotype**: `Resistant`

**Visible annotator hits the agent gets to see:**

| Source | Gene | Class / Subclass / Phenotype | Identity / Cov | Method |
| --- | --- | --- | --- | --- |
| AMRFinderPlus | `gyrA_S83I` | QUINOLONE / QUINOLONE | 99.8% / 100.0% | POINTX |
| AMRFinderPlus | `oqxA` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 100.0% / 100.0% | EXACTX |
| AMRFinderPlus | `oqxB` | NITROFURAN/PHENICOL/QUINOLONE/TETRACYCLINE / NITROFURANTOIN/PHENICOL/QUINOLONE/TIGECYCLINE | 99.8% / 100.0% | BLASTX |
| AMRFinderPlus | `parC_S80I` | QUINOLONE / QUINOLONE | 99.3% / 98.8% | POINTX |
| AMRFinderPlus | `qnrS1` | QUINOLONE / QUINOLONE | 100.0% / 100.0% | ALLELEX |

**Heuristic gold:** `target_modification` · required_genes=['gyras83i', 'parcs80i']

> _Heuristic rationale:_ QRDR mutation in gyrase or topoisomerase IV target reduces fluoroquinolone binding.

_Coverage context: agent saw 5 drug-relevant hits; the underlying isolate has 29 total AMRFinder + 24 total ResFinder hits._

---
