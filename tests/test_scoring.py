from __future__ import annotations

import unittest

from amr_bench.scoring import aggregate_scores, score_output


class ScoringTests(unittest.TestCase):
    def test_genopheno_score(self) -> None:
        task = {"task_id": "t1", "track": "genopheno", "gold": {"phenotype": "Resistant"}}
        output = {
            "task_id": "t1",
            "answer": "Resistant",
            "phenotype_prediction": "Resistant",
            "confidence": 0.8,
            "evidence": [],
            "rationale": "x",
            "uncertainty": "x",
        }
        scored = score_output(task, output)
        self.assertTrue(scored["correct"])

    def test_aggregate_scores(self) -> None:
        summary = aggregate_scores(
            [
                {"track": "genopheno", "json_valid": True, "correct": True, "evidence_items": 1},
                {"track": "genopheno", "json_valid": True, "correct": False, "evidence_items": 3},
            ]
        )
        self.assertEqual(summary["overall"]["n"], 2)
        self.assertEqual(summary["overall"]["accuracy"], 0.5)


if __name__ == "__main__":
    unittest.main()
