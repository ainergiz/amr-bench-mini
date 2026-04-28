"""LLM agent runner for AMR-Bench-mini.

This module provides a minimal, provider-agnostic agent loop that takes a
task dict (from `data/tasks/*.jsonl`) and produces a model output dict that
satisfies `validate_output`. The actual inference is delegated to a callable
``model_fn(messages: list[dict]) -> str`` so this module stays free of any
particular SDK dependency. Tests cover the response parser without making
network calls.

Tools (Day-2 wrappers — call out to optional binaries / web APIs):
    - amrfinder_lookup    : returns precomputed AMRFinder hits for the isolate
    - resfinder_lookup    : returns precomputed ResFinder hits for the isolate
    - card_aro_lookup     : look up ARO mechanism category for a gene name
    - blast_regulator     : run BLAST against reference regulator ORFs
    - alphafold_lookup    : fetch UniProt/AlphaFold structure summary for a protein
    - paperqa_search      : retrieve mechanism citations from a local corpus

Only ``amrfinder_lookup`` and ``resfinder_lookup`` are guaranteed to work
without external dependencies; the others raise NotImplementedError until
their wrappers are written.
"""
from __future__ import annotations

import json
import re
from typing import Any, Callable, Iterable

from amr_bench.prompts import (
    AMR_SCAFFOLDED_SYSTEM_PROMPT,
    DBRECONCILE_INSTRUCTIONS,
    GENERIC_SYSTEM_PROMPT,
    GENOPHENO_INSTRUCTIONS,
    MECHREASON_INSTRUCTIONS,
)


ModelFn = Callable[[list[dict[str, str]]], str]


def build_messages(
    task: dict[str, Any],
    scaffolded: bool = True,
    *,
    card_substrate_context: bool = False,
) -> list[dict[str, str]]:
    """Render a task into chat messages with track-specific instructions.

    When ``card_substrate_context`` is true, a deterministic CARD ARO substrate
    annotation block for every visible relevant_tool_hits gene is appended to
    the user message. This is the no-orchestration variant of the
    "tool-augmented" condition: substrate context is pre-resolved and injected
    as text, so the experiment isolates information availability from any
    tool-calling behavior.
    """
    track = task.get("track")
    instructions = {
        "genopheno": GENOPHENO_INSTRUCTIONS,
        "dbreconcile": DBRECONCILE_INSTRUCTIONS,
        "mechreason": MECHREASON_INSTRUCTIONS,
    }.get(track, "Solve the task using only provided evidence.")

    system = AMR_SCAFFOLDED_SYSTEM_PROMPT if scaffolded else GENERIC_SYSTEM_PROMPT
    user_payload = render_user_payload(task)
    schema = output_schema_block(track)
    parts = [
        instructions,
        "",
        "Output a single JSON object that matches this schema exactly:",
        f"```json\n{schema}\n```",
    ]
    if card_substrate_context:
        block = build_card_substrate_block(task)
        if block:
            parts += ["", block]
    parts += [
        "",
        "Task input:",
        f"```json\n{user_payload}\n```",
        "",
        "Return only the JSON object — no prose before or after it.",
    ]
    user = "\n".join(parts)
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def build_card_substrate_block(task: dict[str, Any]) -> str:
    """Pre-resolve CARD ARO substrate annotations for every visible gene."""
    from amr_bench.tools.card_substrate import render_context_block

    visible = task.get("visible_evidence") or {}
    hits = visible.get("relevant_tool_hits") or []
    genes: list[str] = []
    for hit in hits:
        if not isinstance(hit, dict):
            continue
        for field in ("gene", "element_symbol", "element_name"):
            value = hit.get(field)
            if value and value not in genes:
                genes.append(str(value))
                break
    if not genes:
        return ""
    return render_context_block(genes)


def output_schema_block(track: str | None) -> str:
    """Return a concrete JSON example demonstrating the required output shape.

    Models follow concrete schemas more reliably than prose field lists; in
    particular, they are prone to nesting ``evidence`` as a dict-of-categories
    instead of a flat list of objects when the prompt only names the field.
    """
    common_fields = {
        "task_id": "<string, copy from task>",
        "answer": "<short string, one phrase>",
        "confidence": 0.5,
        "evidence": [
            {"source": "AMRFinderPlus or ResFinder or literature", "gene": "<string>", "claim": "<string>", "supports_answer": True}
        ],
        "rationale": "<string>",
        "uncertainty": "<string describing remaining uncertainty>",
    }
    if track == "genopheno":
        common_fields["phenotype_prediction"] = "Resistant"
        return json.dumps(common_fields, indent=2)
    if track == "dbreconcile":
        common_fields["disagreement_type"] = "drug_mapping_difference"
        common_fields["reconciled_call"] = "<string>"
        return json.dumps(common_fields, indent=2)
    if track == "mechreason":
        common_fields["mechanism_class"] = "enzymatic_inactivation"
        common_fields["layers"] = {
            "genome": "<which gene/variant; chromosomal vs plasmid context if visible>",
            "protein": "<protein identity, native function, structural class, variant impact>",
            "mechanism": "<catalytic / binding / efflux mechanism; substrate specificity if relevant>",
            "cell": "<cellular compartment, pathway interactions, regulators upstream>",
            "phenotype": "<chain from molecular event to observed MIC>",
        }
        common_fields["tools_called"] = []
        return json.dumps(common_fields, indent=2)
    return json.dumps(common_fields, indent=2)


def required_output_fields(track: str | None) -> str:
    """Backward-compat helper retained for tests; new code uses ``output_schema_block``."""
    base = ["task_id", "answer", "confidence", "evidence", "rationale", "uncertainty"]
    if track == "genopheno":
        base += ["phenotype_prediction"]
    elif track == "dbreconcile":
        base += ["disagreement_type", "reconciled_call"]
    elif track == "mechreason":
        base += ["mechanism_class", "layers (object with keys genome, protein, mechanism, cell, phenotype)"]
    return ", ".join(base)


def render_user_payload(task: dict[str, Any]) -> str:
    """Strip labels, provenance, and split metadata before showing a task."""
    hidden_fields = {"gold", "provenance", "hard_split"}
    visible = {k: v for k, v in task.items() if k not in hidden_fields}
    return json.dumps(visible, indent=2, default=str)


def run_agent(task: dict[str, Any], model_fn: ModelFn, scaffolded: bool = True) -> dict[str, Any]:
    """Run a single task through the agent loop and return a parsed output dict."""
    messages = build_messages(task, scaffolded=scaffolded)
    raw = model_fn(messages)
    parsed = parse_json_response(raw)
    if "task_id" not in parsed:
        parsed["task_id"] = task.get("task_id")
    return parsed


def parse_json_response(text: str) -> dict[str, Any]:
    """Extract the first JSON object from a model response.

    Tolerates markdown code fences and prose around the JSON. Returns an empty
    dict with an ``__parse_error`` field on failure so callers can record the
    failure mode without raising.
    """
    if not text:
        return {"__parse_error": "empty response"}
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        candidate = fence.group(1)
    else:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return {"__parse_error": "no JSON object found", "__raw": text[:500]}
        candidate = match.group(0)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as err:
        return {"__parse_error": f"json decode error: {err}", "__raw": candidate[:500]}


# ---------------------------------------------------------------------------
# Provider adapters — kept simple and optional. Tests do not exercise these.

def make_anthropic_model(model: str = "claude-sonnet-4-6", max_tokens: int = 2048) -> ModelFn:
    """Return a model_fn that calls Anthropic's Messages API.

    Requires ``ANTHROPIC_API_KEY`` env var and the ``anthropic`` SDK.
    """
    try:
        import anthropic  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional dep
        raise RuntimeError("anthropic package not installed; pip install anthropic") from exc

    client = anthropic.Anthropic()

    def call(messages: list[dict[str, str]]) -> str:
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_messages = [m for m in messages if m["role"] != "system"]
        result = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": m["role"], "content": m["content"]} for m in user_messages],
        )
        return "".join(block.text for block in result.content if getattr(block, "type", "") == "text")

    return call


def make_openai_model(model: str = "gpt-5", max_tokens: int = 2048) -> ModelFn:  # pragma: no cover - optional
    try:
        from openai import OpenAI  # type: ignore
    except ImportError as exc:
        raise RuntimeError("openai package not installed; pip install openai") from exc

    client = OpenAI()

    def call(messages: list[dict[str, str]]) -> str:
        result = client.chat.completions.create(model=model, max_tokens=max_tokens, messages=messages)
        return result.choices[0].message.content or ""

    return call


# ---------------------------------------------------------------------------
# Iteration helpers

def run_batch(tasks: Iterable[dict[str, Any]], model_fn: ModelFn, scaffolded: bool = True) -> list[dict[str, Any]]:
    return [run_agent(task, model_fn, scaffolded=scaffolded) for task in tasks]
