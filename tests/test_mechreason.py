"""Tests for MechReason task building and scoring."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from amr_bench.scoring import score_output  # noqa: E402
from amr_bench.schema import MECHREASON_LAYERS, validate_task  # noqa: E402
from build_tasks import infer_mechanism  # noqa: E402


class InferMechanismTests(unittest.TestCase):
    def test_carbapenemase_to_enzymatic_inactivation(self) -> None:
        hits = [
            {"source": "AMRFinderPlus", "gene": "blaKPC-2", "drug_class": "BETA-LACTAM", "subclass": "CARBAPENEM", "method": "ALLELEX"},
        ]
        cls, required, _ = infer_mechanism("meropenem", hits)
        self.assertEqual(cls, "enzymatic_inactivation")
        self.assertIn("blakpc2", required)

    def test_porin_loss_priority(self) -> None:
        hits = [
            {"source": "AMRFinderPlus", "gene": "blaSHV-11", "drug_class": "BETA-LACTAM", "subclass": "BETA-LACTAM", "method": "ALLELEX"},
            {"source": "AMRFinderPlus", "gene": "ompK35_E42RfsTer47", "drug_class": "BETA-LACTAM", "subclass": "CARBAPENEM", "method": "POINTX"},
        ]
        cls, required, _ = infer_mechanism("meropenem", hits)
        self.assertEqual(cls, "permeability_loss")
        self.assertTrue(any("ompk" in r for r in required))

    def test_qrdr_target_modification(self) -> None:
        hits = [
            {"source": "AMRFinderPlus", "gene": "gyrA_S83Y", "drug_class": "QUINOLONE", "subclass": "QUINOLONE", "method": "POINTX"},
            {"source": "AMRFinderPlus", "gene": "parC_S80I", "drug_class": "QUINOLONE", "subclass": "QUINOLONE", "method": "POINTX"},
        ]
        cls, required, _ = infer_mechanism("ciprofloxacin", hits)
        self.assertEqual(cls, "target_modification")

    def test_regulator_lof_priority(self) -> None:
        hits = [
            {"source": "AMRFinderPlus", "gene": "ramR_E102SfsTer17", "drug_class": "MULTIDRUG", "subclass": "TIGECYCLINE", "method": "POINTX"},
        ]
        cls, required, _ = infer_mechanism("tigecycline", hits)
        self.assertEqual(cls, "regulator_loss_of_function")

    def test_no_relevant_hits_yields_insufficient(self) -> None:
        cls, required, _ = infer_mechanism("tigecycline", [])
        self.assertEqual(cls, "insufficient_evidence")
        self.assertEqual(required, [])

    def test_dfrA_metabolic_bypass(self) -> None:
        hits = [
            {"source": "AMRFinderPlus", "gene": "dfrA1", "drug_class": "TRIMETHOPRIM", "subclass": "TRIMETHOPRIM", "method": "EXACTX"},
        ]
        cls, required, _ = infer_mechanism("trimethoprim/sulfamethoxazole", hits)
        self.assertEqual(cls, "metabolic_bypass")

    def test_tetracycline_with_teta_and_ramR_is_efflux_not_regulator(self) -> None:
        """Direct drug-specific tet(A) wins over regulator LoF for tetracycline."""
        hits = [
            {"source": "AMRFinderPlus", "gene": "tet(A)", "drug_class": "TETRACYCLINE", "subclass": "TETRACYCLINE", "method": "EXACTX"},
            {"source": "AMRFinderPlus", "gene": "ramR_E113PfsTer7", "drug_class": "MULTIDRUG", "subclass": "TETRACYCLINE", "method": "POINTX"},
        ]
        cls, required, _ = infer_mechanism("tetracycline", hits)
        self.assertEqual(cls, "efflux")
        self.assertTrue(any("teta" in r for r in required))

    def test_tigecycline_with_only_wildtype_teta_is_insufficient(self) -> None:
        """Wild-type tet(A) cannot drive tigecycline R; HypothesisGen flavor."""
        hits = [
            {"source": "AMRFinderPlus", "gene": "tet(A)", "drug_class": "TETRACYCLINE", "subclass": "TETRACYCLINE", "method": "EXACTX"},
            {"source": "AMRFinderPlus", "gene": "oqxA", "drug_class": "TETRACYCLINE", "subclass": "TIGECYCLINE", "method": "EXACTX"},
        ]
        cls, required, _ = infer_mechanism("tigecycline", hits)
        self.assertEqual(cls, "insufficient_evidence")

    def test_tigecycline_with_ramR_LoF_is_regulator_lof(self) -> None:
        """ramR LoF + tigecycline → modal published mechanism."""
        hits = [
            {"source": "AMRFinderPlus", "gene": "tet(A)", "drug_class": "TETRACYCLINE", "subclass": "TETRACYCLINE", "method": "EXACTX"},
            {"source": "AMRFinderPlus", "gene": "ramR_Y59CfsTer13", "drug_class": "MULTIDRUG", "subclass": "TIGECYCLINE", "method": "POINTX"},
        ]
        cls, _, _ = infer_mechanism("tigecycline", hits)
        self.assertEqual(cls, "regulator_loss_of_function")

    def test_cefoxitin_with_kpc_is_enzymatic_inactivation(self) -> None:
        """KPC-2/3 hydrolyze cefoxitin; should be enzymatic_inactivation, not permeability_loss."""
        hits = [
            {"source": "AMRFinderPlus", "gene": "blaKPC-2", "drug_class": "BETA-LACTAM", "subclass": "CARBAPENEM", "method": "ALLELEX"},
            {"source": "AMRFinderPlus", "gene": "blaSHV-1", "drug_class": "BETA-LACTAM", "subclass": "BETA-LACTAM", "method": "ALLELEX"},
            {"source": "AMRFinderPlus", "gene": "ompK35_E42RfsTer47", "drug_class": "BETA-LACTAM", "subclass": "CARBAPENEM", "method": "POINTX"},
        ]
        cls, _, _ = infer_mechanism("cefoxitin", hits)
        self.assertEqual(cls, "enzymatic_inactivation")

    def test_cefoxitin_with_only_esbl_and_porin_loss_is_permeability(self) -> None:
        """ESBLs (CTX-M, narrow SHV/TEM/OXA) do not hydrolyze cefoxitin; porin loss dominates."""
        hits = [
            {"source": "AMRFinderPlus", "gene": "blaCTX-M-15", "drug_class": "BETA-LACTAM", "subclass": "CEPHALOSPORIN", "method": "ALLELEX"},
            {"source": "AMRFinderPlus", "gene": "blaSHV-52", "drug_class": "BETA-LACTAM", "subclass": "BETA-LACTAM", "method": "ALLELEX"},
            {"source": "AMRFinderPlus", "gene": "ompK36_Q313Ter", "drug_class": "BETA-LACTAM", "subclass": "CARBAPENEM", "method": "POINTX"},
        ]
        cls, _, _ = infer_mechanism("cefoxitin", hits)
        self.assertEqual(cls, "permeability_loss")

    def test_cefoxitin_with_ampc_is_enzymatic_inactivation(self) -> None:
        hits = [
            {"source": "AMRFinderPlus", "gene": "blaCMY-2", "drug_class": "BETA-LACTAM", "subclass": "CEPHALOSPORIN", "method": "ALLELEX"},
        ]
        cls, _, _ = infer_mechanism("cefoxitin", hits)
        self.assertEqual(cls, "enzymatic_inactivation")

    def test_ampicillin_with_carbapenemase_is_enzymatic_not_permeability(self) -> None:
        """Regression: porin loss should not override β-lactamase for non-carbapenems."""
        hits = [
            {"source": "AMRFinderPlus", "gene": "blaKPC-2", "drug_class": "BETA-LACTAM", "subclass": "CARBAPENEM", "method": "ALLELEX"},
            {"source": "AMRFinderPlus", "gene": "blaCTX-M-15", "drug_class": "BETA-LACTAM", "subclass": "CEPHALOSPORIN", "method": "ALLELEX"},
            {"source": "AMRFinderPlus", "gene": "ompK35_G208VfsTer5", "drug_class": "BETA-LACTAM", "subclass": "CARBAPENEM", "method": "POINTX"},
        ]
        cls, _, _ = infer_mechanism("ampicillin", hits)
        self.assertEqual(cls, "enzymatic_inactivation")


class MechreasonScoringTests(unittest.TestCase):
    def _task(self, mechanism_class: str = "enzymatic_inactivation", required: list[str] | None = None) -> dict:
        return {
            "task_id": "mechreason_test_1",
            "track": "mechreason",
            "species": "Klebsiella pneumoniae",
            "genome_id": "0.0",
            "genome_name": "test",
            "assembly_path": "data/fasta/0.0.fna",
            "antibiotic": "meropenem",
            "antibiotic_class": "beta-lactam",
            "metadata": {},
            "visible_evidence": {"labels_visible": False, "phenotype_visible": True, "ast_phenotype": "Resistant", "relevant_tool_hits": []},
            "gold": {
                "phenotype": "Resistant",
                "mechanism_class": mechanism_class,
                "required_genes": required if required is not None else ["blakpc2"],
                "rationale": "test",
            },
            "provenance": {},
        }

    def test_full_score_when_all_layers_and_class_match(self) -> None:
        task = self._task()
        output = {
            "task_id": "mechreason_test_1",
            "answer": "enzymatic_inactivation",
            "mechanism_class": "enzymatic_inactivation",
            "layers": {layer: f"{layer} content" for layer in MECHREASON_LAYERS},
            "evidence": [{"source": "AMRFinderPlus", "gene": "blaKPC-2", "claim": "blaKPC-2 hydrolyzes meropenem"}],
            "rationale": " ".join(MECHREASON_LAYERS),
            "uncertainty": "low",
            "confidence": 0.9,
        }
        result = score_output(task, output)
        self.assertTrue(result["mechanism_class_correct"])
        self.assertTrue(result["gene_family_correct"])
        self.assertTrue(result["layers_complete"])
        self.assertTrue(result["correct"])

    def test_layers_incomplete_disqualifies_composite(self) -> None:
        task = self._task()
        output = {
            "task_id": "mechreason_test_1",
            "answer": "enzymatic_inactivation",
            "mechanism_class": "enzymatic_inactivation",
            "layers": {"genome": "g", "protein": "p"},  # only 2 of 5
            "evidence": [{"gene": "blaKPC-2", "source": "AMRFinderPlus", "claim": "blaKPC-2 hits"}],
            "rationale": "genome protein only",
            "uncertainty": "low",
            "confidence": 0.9,
        }
        result = score_output(task, output)
        self.assertTrue(result["mechanism_class_correct"])
        self.assertFalse(result["layers_complete"])
        self.assertFalse(result["correct"])

    def test_insufficient_evidence_grants_credit_without_required_gene(self) -> None:
        task = self._task(mechanism_class="insufficient_evidence", required=[])
        output = {
            "task_id": "mechreason_test_1",
            "answer": "insufficient_evidence",
            "mechanism_class": "insufficient_evidence",
            "layers": {layer: f"{layer} content" for layer in MECHREASON_LAYERS},
            "evidence": [],
            "rationale": " ".join(MECHREASON_LAYERS),
            "uncertainty": "high",
            "confidence": 0.4,
        }
        result = score_output(task, output)
        self.assertTrue(result["mechanism_class_correct"])
        self.assertTrue(result["correct"])


class MechreasonValidationTests(unittest.TestCase):
    def test_invalid_mechanism_class_rejected(self) -> None:
        task = {
            "task_id": "x",
            "track": "mechreason",
            "species": "Klebsiella pneumoniae",
            "genome_id": "0.0",
            "genome_name": "n",
            "assembly_path": "p",
            "antibiotic": "meropenem",
            "visible_evidence": {},
            "gold": {"phenotype": "Resistant", "mechanism_class": "made_up_class", "required_genes": []},
            "provenance": {},
        }
        errors = validate_task(task)
        self.assertTrue(any("invalid mechanism_class" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
