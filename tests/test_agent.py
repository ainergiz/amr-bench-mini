"""Tests for the LLM agent harness — covers prompt building and JSON parsing only."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.agent import build_messages, parse_json_response, render_user_payload, run_agent  # noqa: E402


class ParseJsonResponseTests(unittest.TestCase):
    def test_extracts_fenced_json(self) -> None:
        text = "Some prose.\n```json\n{\"task_id\": \"x\", \"answer\": \"foo\"}\n```\nMore prose."
        result = parse_json_response(text)
        self.assertEqual(result["answer"], "foo")

    def test_extracts_unfenced_json(self) -> None:
        text = "Here it is: {\"task_id\": \"y\", \"value\": 1}"
        result = parse_json_response(text)
        self.assertEqual(result["task_id"], "y")

    def test_returns_parse_error_on_garbage(self) -> None:
        result = parse_json_response("no json here")
        self.assertIn("__parse_error", result)

    def test_returns_parse_error_on_invalid_json(self) -> None:
        result = parse_json_response("{bad json,")
        self.assertIn("__parse_error", result)


class BuildMessagesTests(unittest.TestCase):
    def test_mechreason_messages_contain_layer_instructions(self) -> None:
        task = {
            "task_id": "x",
            "track": "mechreason",
            "antibiotic": "meropenem",
            "visible_evidence": {"relevant_tool_hits": []},
        }
        messages = build_messages(task)
        joined = " ".join(m["content"] for m in messages)
        for layer in ("L1 Genome", "L2 Protein", "L3 Mechanism", "L4 Cell", "L5 Phenotype"):
            self.assertIn(layer, joined)

    def test_user_payload_strips_gold(self) -> None:
        task = {
            "task_id": "y",
            "track": "mechreason",
            "antibiotic": "meropenem",
            "visible_evidence": {"relevant_tool_hits": []},
            "gold": {"mechanism_class": "enzymatic_inactivation"},
            "provenance": {"data_source": "test"},
            "hard_split": {
                "category": "hypothesisgen_insufficient_evidence",
                "rationale": "this would leak the hard split label",
            },
        }
        payload = render_user_payload(task)
        self.assertNotIn("mechanism_class", payload)
        self.assertNotIn("provenance", payload)
        self.assertNotIn("hard_split", payload)
        self.assertNotIn("hypothesisgen_insufficient_evidence", payload)
        self.assertIn("antibiotic", payload)

    def test_run_agent_passes_through_fake_model(self) -> None:
        task = {
            "task_id": "z",
            "track": "genopheno",
            "antibiotic": "meropenem",
            "visible_evidence": {"relevant_tool_hits": []},
        }

        def fake_model(messages: list[dict[str, str]]) -> str:
            return '{"task_id": "z", "answer": "Susceptible", "phenotype_prediction": "Susceptible", "confidence": 0.5, "evidence": [], "rationale": "test", "uncertainty": "high"}'

        result = run_agent(task, fake_model)
        self.assertEqual(result["phenotype_prediction"], "Susceptible")


if __name__ == "__main__":
    unittest.main()
