from __future__ import annotations

import unittest

from amr_bench.schema import validate_output, validate_task


class SchemaTests(unittest.TestCase):
    def test_genopheno_task_validates(self) -> None:
        task = {
            "task_id": "genopheno_kp_000001",
            "track": "genopheno",
            "species": "Klebsiella pneumoniae",
            "genome_id": "573.1",
            "genome_name": "example",
            "assembly_path": "data/fasta/573.1.fna",
            "antibiotic": "ceftriaxone",
            "visible_evidence": {},
            "gold": {"phenotype": "Resistant"},
            "provenance": {},
        }
        self.assertEqual(validate_task(task), [])

    def test_output_requires_confidence_range(self) -> None:
        output = {
            "task_id": "x",
            "answer": "Resistant",
            "confidence": 2,
            "evidence": [],
            "rationale": "",
            "uncertainty": "",
        }
        self.assertIn("confidence must be a number in [0, 1]", validate_output(output))


if __name__ == "__main__":
    unittest.main()
