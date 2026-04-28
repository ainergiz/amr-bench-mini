from __future__ import annotations

import unittest

from amr_bench.parsing import gene_family, hit_matches_antibiotic


class ParsingTests(unittest.TestCase):
    def test_gene_family_normalizes_common_amr_names(self) -> None:
        self.assertEqual(gene_family("blaSHV-11"), "blashv")
        self.assertEqual(gene_family("blaSHV_C-112A"), "blashv")
        self.assertEqual(gene_family("oqxB25"), "oqxb")

    def test_amrfinder_beta_lactam_hit_matches_ceftriaxone(self) -> None:
        hit = {"source": "AMRFinderPlus", "drug_class": "BETA-LACTAM", "subclass": "CEPHALOSPORIN"}
        self.assertTrue(hit_matches_antibiotic(hit, "ceftriaxone"))

    def test_resfinder_phenotype_hit_matches_combo_alias(self) -> None:
        hit = {"source": "ResFinder", "phenotype": "Piperacillin+Tazobactam"}
        self.assertTrue(hit_matches_antibiotic(hit, "piperacillin/tazobactam"))


if __name__ == "__main__":
    unittest.main()
