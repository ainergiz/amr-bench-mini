#!/usr/bin/env python3
"""Run an LLM agent over MechReason tasks and score the outputs.

Usage:
    # Smoke test (3 tasks, mocked model — no API key needed)
    python3 scripts/run_llm_eval.py --smoke

    # Pilot run (50 tasks, real API)
    python3 scripts/run_llm_eval.py --pilot --provider anthropic --model claude-sonnet-4-6

    # Custom: take first N tasks from a JSONL file
    python3 scripts/run_llm_eval.py --tasks-file data/tasks/mechreason.jsonl --limit 20 \\
        --provider anthropic --model claude-haiku-4-5-20251001

Required env vars:
    ANTHROPIC_API_KEY   for --provider anthropic
    OPENAI_API_KEY      for --provider openai

Outputs (under results/llm_eval/<run_name>/):
    raw_outputs.jsonl              - per-task row with the full task snapshot, model output,
                                     score, latency_s, and provider-reported token usage
    summary.json                   - aggregate metrics, per-class breakdown, usage totals
    summary.md                     - human-readable summary table
    manifest.json                  - command-line, model params, prompt SHA-16s, task SHA-16,
                                     full task_id list, timestamp
    prompts.txt                    - verbatim system + track-instruction prompt text
    tasks_used.jsonl               - frozen copy of the exact task subset that was scored
    dataset_summary_snapshot.json  - corpus-level snapshot at run time
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.agent import build_messages, parse_json_response  # noqa: E402
from amr_bench.io import read_jsonl, write_json, write_jsonl  # noqa: E402
from amr_bench.pricing import cost_estimate  # noqa: E402
from amr_bench.scoring import aggregate_scores, score_output  # noqa: E402

DATA = ROOT / "data"
TASKS = DATA / "tasks"
RESULTS = ROOT / "results" / "llm_eval"


def load_dotenv_local() -> None:
    """Load simple KEY=VALUE pairs from .env.local if the process env lacks them."""
    env_path = ROOT / ".env.local"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().replace("export ", "")
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def main() -> None:
    load_dotenv_local()
    args = parse_args()
    run_name = args.run_name or default_run_name(args)
    out_dir = RESULTS / run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks, source_path = load_tasks(args)
    print(f"Loaded {len(tasks)} tasks from {describe_source(args)}")
    print(f"Output directory: {out_dir}")

    write_manifest(out_dir, args, tasks, source_path, run_name)

    model_fn = build_model_fn(args)
    rows = []
    scored = []
    usage_totals: dict[str, int] = defaultdict(int)
    print()
    for i, task in enumerate(tasks, 1):
        t0 = time.time()
        usage: dict = {}
        try:
            messages = build_messages(task, scaffolded=True, card_substrate_context=args.card_substrate_context)
            raw, usage = model_fn(messages)
            parsed = parse_json_response(raw)
            if "task_id" not in parsed:
                parsed["task_id"] = task["task_id"]
        except Exception as exc:
            parsed = {"task_id": task["task_id"], "__call_error": str(exc)}
            raw = ""
        latency = time.time() - t0
        for k, v in (usage or {}).items():
            if isinstance(v, (int, float)):
                usage_totals[k] += int(v)
        score = score_output(task, parsed)
        rows.append({
            "task_id": task["task_id"],
            "track": task["track"],
            "task": task,
            "gold": task["gold"],
            "model": args.model,
            "provider": args.provider,
            "output": parsed,
            "raw_response": raw if args.save_raw else None,
            "score": score,
            "latency_s": round(latency, 3),
            "usage": usage,
        })
        scored.append(score)
        if i <= 3 or i % 10 == 0 or i == len(tasks):
            mark = "✓" if score.get("correct") else "✗"
            class_label = ""
            if task["track"] == "mechreason":
                class_label = f" gold={task['gold']['mechanism_class']:25s} pred={parsed.get('mechanism_class','?'):25s}"
            print(f"  [{i:>3}/{len(tasks)}] {mark} {task['task_id']}{class_label} ({latency:.1f}s)")

    summary = aggregate_scores(scored)
    summary["run_name"] = run_name
    summary["provider"] = args.provider
    summary["model"] = args.model
    summary["n_tasks"] = len(tasks)
    summary["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    summary["usage_totals"] = dict(usage_totals)
    summary["cost_estimate_usd"] = cost_estimate(args.model, args.provider, dict(usage_totals))
    if args.smoke:
        summary["mode"] = "smoke (real API)" if args.provider != "mock" else "smoke (mocked model)"

    if any(t["track"] == "mechreason" for t in tasks):
        summary["mechreason_breakdown"] = mechreason_breakdown(rows)

    write_jsonl(out_dir / "raw_outputs.jsonl", rows)
    write_json(out_dir / "summary.json", summary)
    (out_dir / "summary.md").write_text(render_summary_md(summary))

    print()
    print(render_summary_md(summary))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--smoke", action="store_true", help="3-task smoke test with mocked model (no API key needed).")
    src.add_argument("--pilot", action="store_true", help="Use the frozen 50-task MechReason pilot subset.")
    src.add_argument("--tasks-file", type=Path, help="JSONL of tasks to run.")
    p.add_argument("--limit", type=int, default=None, help="Cap the number of tasks (after stratified sampling already applied).")
    p.add_argument("--provider", choices=["anthropic", "openai", "gemini", "mock"], default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--run-name", default=None)
    p.add_argument("--save-raw", action="store_true", help="Persist raw response strings (off by default to keep JSONL small).")
    p.add_argument(
        "--card-substrate-context",
        action="store_true",
        help="Inject a deterministic CARD ARO substrate-annotation block for every visible "
             "tool-hit gene into the prompt. Tool-augmented variant.",
    )
    args = p.parse_args()
    if args.smoke:
        args.provider = args.provider or "mock"
        args.model = args.model or "smoke-mock-v1"
    else:
        if not args.provider:
            p.error("--provider is required unless --smoke is used")
        if not args.model:
            p.error("--model is required unless --smoke is used")
    return args


def default_run_name(args: argparse.Namespace) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.smoke:
        return f"smoke_{stamp}"
    short = args.model.replace("/", "-").replace(":", "-")
    if args.pilot:
        return f"pilot_{short}_{stamp}"
    return f"adhoc_{short}_{stamp}"


def load_tasks(args: argparse.Namespace) -> tuple[list[dict], Path | None]:
    if args.smoke:
        return smoke_test_tasks(), None
    if args.pilot:
        path = TASKS / "mechreason_pilot.jsonl"
    else:
        path = args.tasks_file
    if not path or not path.exists():
        raise SystemExit(f"Tasks file not found: {path}")
    tasks = read_jsonl(path)
    if args.limit:
        tasks = tasks[: args.limit]
    return tasks, path


def describe_source(args: argparse.Namespace) -> str:
    if args.smoke:
        return "smoke-test fixtures (3 tasks)"
    if args.pilot:
        return "data/tasks/mechreason_pilot.jsonl"
    return str(args.tasks_file)


def write_manifest(out_dir: Path, args: argparse.Namespace, tasks: list[dict], source_path: Path | None, run_name: str) -> None:
    """Freeze command-line args, model params, prompt versions, and the task subset for reproducibility."""
    import hashlib

    from amr_bench.prompts import (
        AMR_SCAFFOLDED_SYSTEM_PROMPT,
        DBRECONCILE_INSTRUCTIONS,
        GENERIC_SYSTEM_PROMPT,
        GENOPHENO_INSTRUCTIONS,
        MECHREASON_INSTRUCTIONS,
    )

    task_blob = "\n".join(json.dumps(t, sort_keys=True, default=str) for t in tasks)
    task_sha = hashlib.sha256(task_blob.encode()).hexdigest()[:16]

    manifest = {
        "run_name": run_name,
        "command": " ".join(sys.argv),
        "argv": sys.argv,
        "args": {
            "smoke": args.smoke,
            "pilot": args.pilot,
            "tasks_file": str(source_path) if source_path else None,
            "limit": args.limit,
            "provider": args.provider,
            "model": args.model,
            "max_tokens": args.max_tokens,
            "save_raw": args.save_raw,
            "card_substrate_context": args.card_substrate_context,
        },
        "n_tasks": len(tasks),
        "task_subset_sha256_16": task_sha,
        "task_id_list": [t["task_id"] for t in tasks],
        "prompt_versions": {
            "AMR_SCAFFOLDED_SYSTEM_PROMPT_sha16": _sha16(AMR_SCAFFOLDED_SYSTEM_PROMPT),
            "GENERIC_SYSTEM_PROMPT_sha16": _sha16(GENERIC_SYSTEM_PROMPT),
            "MECHREASON_INSTRUCTIONS_sha16": _sha16(MECHREASON_INSTRUCTIONS),
            "GENOPHENO_INSTRUCTIONS_sha16": _sha16(GENOPHENO_INSTRUCTIONS),
            "DBRECONCILE_INSTRUCTIONS_sha16": _sha16(DBRECONCILE_INSTRUCTIONS),
        },
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(out_dir / "manifest.json", manifest)
    # Also persist full prompt text for word-for-word reproducibility.
    (out_dir / "prompts.txt").write_text(
        "===== AMR_SCAFFOLDED_SYSTEM_PROMPT =====\n" + AMR_SCAFFOLDED_SYSTEM_PROMPT + "\n\n"
        "===== GENERIC_SYSTEM_PROMPT =====\n" + GENERIC_SYSTEM_PROMPT + "\n\n"
        "===== MECHREASON_INSTRUCTIONS =====\n" + MECHREASON_INSTRUCTIONS + "\n\n"
        "===== GENOPHENO_INSTRUCTIONS =====\n" + GENOPHENO_INSTRUCTIONS + "\n\n"
        "===== DBRECONCILE_INSTRUCTIONS =====\n" + DBRECONCILE_INSTRUCTIONS + "\n"
    )
    # Freeze the exact task subset that was scored.
    write_jsonl(out_dir / "tasks_used.jsonl", tasks)
    # Snapshot the dataset summary at run time so future readers can tie the
    # subset to the corpus state.
    dataset_summary = ROOT / "outputs" / "dataset_summary.json"
    if dataset_summary.exists():
        (out_dir / "dataset_summary_snapshot.json").write_text(dataset_summary.read_text())


def _sha16(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def build_model_fn(args: argparse.Namespace):
    if args.provider == "mock":
        return mock_model_fn()
    if args.provider == "anthropic":
        return build_anthropic_model_fn(args)
    if args.provider == "openai":
        return build_openai_model_fn(args)
    if args.provider == "gemini":
        return build_gemini_model_fn(args)
    raise ValueError(f"unknown provider {args.provider}")


def build_anthropic_model_fn(args):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY env var not set; cannot use --provider anthropic")
    try:
        import anthropic  # type: ignore
    except ImportError:
        raise SystemExit("anthropic SDK not installed; pip install anthropic")
    client = anthropic.Anthropic()

    def call(messages):
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]
        result = client.messages.create(
            model=args.model,
            max_tokens=args.max_tokens,
            system=system,
            messages=[{"role": m["role"], "content": m["content"]} for m in user_msgs],
        )
        text = "".join(block.text for block in result.content if getattr(block, "type", "") == "text")
        usage = {}
        if getattr(result, "usage", None):
            usage = {
                "input_tokens": getattr(result.usage, "input_tokens", None),
                "output_tokens": getattr(result.usage, "output_tokens", None),
            }
            # Cache + thinking buckets when present.
            for extra in ("cache_creation_input_tokens", "cache_read_input_tokens"):
                v = getattr(result.usage, extra, None)
                if v is not None:
                    usage[extra] = v
        return text, usage

    return call


def build_openai_model_fn(args):
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY env var not set; cannot use --provider openai")
    try:
        from openai import OpenAI  # type: ignore
    except ImportError:
        raise SystemExit("openai SDK not installed; pip install openai")
    client = OpenAI()

    # GPT-5 / GPT-5.4 / o-series go through the Responses API; older GPT-4* models
    # still use Chat Completions. The Responses API takes ``instructions`` for the
    # system prompt and ``input`` for user-side messages, and uses
    # ``max_output_tokens`` rather than ``max_tokens``/``max_completion_tokens``.
    use_responses_api = args.model.startswith(("gpt-5", "o3", "o4"))

    def call(messages: list[dict[str, str]]) -> tuple[str, dict]:
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]
        if use_responses_api:
            kwargs = {
                "model": args.model,
                "instructions": system,
                "input": [{"role": m["role"], "content": m["content"]} for m in user_msgs],
                "max_output_tokens": args.max_tokens,
            }
            resp = client.responses.create(**kwargs)
            text = getattr(resp, "output_text", None)
            if not text:
                # Fallback: walk the structured output for text blocks.
                chunks: list[str] = []
                for item in getattr(resp, "output", []) or []:
                    for content in getattr(item, "content", []) or []:
                        text_attr = getattr(content, "text", None)
                        if text_attr:
                            chunks.append(text_attr)
                text = "".join(chunks)
            usage = extract_openai_usage(resp)
            return text, usage
        # Legacy chat completions path
        resp = client.chat.completions.create(
            model=args.model, max_tokens=args.max_tokens, messages=messages
        )
        usage = extract_openai_usage(resp)
        return resp.choices[0].message.content or "", usage

    return call


def extract_openai_usage(resp) -> dict:
    """Return a normalized usage dict from either a Responses or Chat Completions reply."""
    usage = getattr(resp, "usage", None)
    if not usage:
        return {}
    out: dict = {}
    for src_key, dst_key in (
        ("input_tokens", "input_tokens"),
        ("output_tokens", "output_tokens"),
        ("total_tokens", "total_tokens"),
        ("prompt_tokens", "input_tokens"),
        ("completion_tokens", "output_tokens"),
    ):
        val = getattr(usage, src_key, None)
        if val is not None and dst_key not in out:
            out[dst_key] = val
    # Reasoning models report a sub-bucket of output_tokens.
    details = getattr(usage, "output_tokens_details", None)
    if details is not None:
        reasoning = getattr(details, "reasoning_tokens", None)
        if reasoning is not None:
            out["reasoning_tokens"] = reasoning
    return out


def build_gemini_model_fn(args):
    """Adapter for Google Gemini via the ``google-genai`` SDK.

    Uses ``GEMINI_API_KEY`` if present, else ``GOOGLE_GENERATIVE_AI_API_KEY``.
    The Gemini API takes the system prompt via ``config.system_instruction`` and
    user content via the ``contents`` field as parts.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or GOOGLE_GENERATIVE_AI_API_KEY for --provider gemini")
    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
    except ImportError:
        raise SystemExit("google-genai SDK not installed; uv pip install google-genai")
    client = genai.Client(api_key=api_key)

    def call(messages: list[dict[str, str]]) -> tuple[str, dict]:
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]
        contents = [
            {"role": ("model" if m["role"] == "assistant" else "user"), "parts": [{"text": m["content"]}]}
            for m in user_msgs
        ]
        config = types.GenerateContentConfig(
            system_instruction=system or None,
            max_output_tokens=args.max_tokens,
        )
        resp = client.models.generate_content(model=args.model, contents=contents, config=config)
        text = getattr(resp, "text", "") or ""
        usage = {}
        meta = getattr(resp, "usage_metadata", None)
        if meta is not None:
            usage = {
                "input_tokens": getattr(meta, "prompt_token_count", None),
                "output_tokens": getattr(meta, "candidates_token_count", None),
                "total_tokens": getattr(meta, "total_token_count", None),
            }
            thoughts = getattr(meta, "thoughts_token_count", None)
            if thoughts is not None:
                usage["reasoning_tokens"] = thoughts
            usage = {k: v for k, v in usage.items() if v is not None}
        return text, usage

    return call


def mock_model_fn():
    """Deterministic mocked agent that returns canned outputs for smoke testing.

    Real LLM agents will NOT have access to the gold; this mock is for plumbing
    validation only. It demonstrates that the harness ingests tasks, builds
    messages, parses JSON, and scores correctly end-to-end. Returns ``(text, usage)``
    matching the real provider adapters.
    """
    def call(messages):
        # Recover task payload from the user message.
        user_content = next(m["content"] for m in messages if m["role"] != "system")
        # Cheap parse of the embedded JSON task.
        json_start = user_content.rfind("```json\n") + len("```json\n")
        json_end = user_content.rfind("```")
        task = json.loads(user_content[json_start:json_end])
        track = task.get("track")
        mock_usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        if track == "mechreason":
            payload = {
                "task_id": task["task_id"],
                "answer": "enzymatic_inactivation",
                "mechanism_class": "enzymatic_inactivation",
                "layers": {
                    "genome": "Mock layer 1.",
                    "protein": "Mock layer 2.",
                    "mechanism": "Mock layer 3.",
                    "cell": "Mock layer 4.",
                    "phenotype": "Mock layer 5.",
                },
                "evidence": [{"source": "mock", "gene": "blamock", "claim": "mocked", "supports_answer": True}],
                "rationale": "Mock rationale; references genome protein mechanism cell phenotype.",
                "uncertainty": "low",
                "confidence": 0.5,
                "tools_called": [],
            }
        elif track == "genopheno":
            payload = {
                "task_id": task["task_id"],
                "answer": "Resistant",
                "phenotype_prediction": "Resistant",
                "evidence": [],
                "rationale": "mock",
                "uncertainty": "high",
                "confidence": 0.5,
            }
        else:
            payload = {
                "task_id": task["task_id"],
                "answer": "drug_mapping_difference",
                "disagreement_type": "drug_mapping_difference",
                "reconciled_call": "mock",
                "evidence": [],
                "rationale": "mock",
                "uncertainty": "high",
                "confidence": 0.5,
            }
        return json.dumps(payload), mock_usage
    return call


def smoke_test_tasks() -> list[dict]:
    pilot = read_jsonl(TASKS / "mechreason_pilot.jsonl")
    if not pilot:
        # Fall back to the full task list
        pilot = read_jsonl(TASKS / "mechreason.jsonl")
    # Pick one of each: hybrid permeability_loss, insufficient_evidence, target_modification.
    chosen: list[dict] = []
    seen_classes: set[str] = set()
    for t in pilot:
        cls = t["gold"]["mechanism_class"]
        is_hybrid = bool(t["gold"].get("secondary_mechanism_classes"))
        key = f"{cls}_hybrid" if is_hybrid else cls
        if key in {"permeability_loss_hybrid", "insufficient_evidence", "target_modification"} and key not in seen_classes:
            chosen.append(t)
            seen_classes.add(key)
        if len(chosen) >= 3:
            break
    return chosen


def mechreason_breakdown(rows: list[dict]) -> dict:
    classes: defaultdict[str, dict] = defaultdict(lambda: {"n": 0, "correct": 0})
    layer_totals = {"mechanism_class_correct": 0, "gene_family_correct": 0, "layers_complete": 0}
    parse_errors = 0
    for r in rows:
        if r["track"] != "mechreason":
            continue
        cls = r["gold"]["mechanism_class"]
        classes[cls]["n"] += 1
        if r["score"].get("correct"):
            classes[cls]["correct"] += 1
        for k in layer_totals:
            if r["score"].get(k):
                layer_totals[k] += 1
        if r["output"].get("__parse_error") or r["output"].get("__call_error"):
            parse_errors += 1
    n_mech = sum(c["n"] for c in classes.values())
    return {
        "n_mechreason": n_mech,
        "by_class": {cls: {**v, "accuracy": (v["correct"] / v["n"]) if v["n"] else 0.0} for cls, v in classes.items()},
        "subscore_rates": {k: (v / n_mech if n_mech else 0.0) for k, v in layer_totals.items()},
        "parse_or_call_errors": parse_errors,
    }


def render_summary_md(summary: dict) -> str:
    lines = [
        f"# LLM eval summary — {summary.get('run_name','?')}",
        "",
        f"- Provider/model: `{summary.get('provider')}` / `{summary.get('model')}`",
        f"- N tasks: {summary.get('n_tasks')}",
        f"- Timestamp: {summary.get('timestamp_utc')}",
    ]
    if summary.get("mode"):
        lines.append(f"- Mode: {summary['mode']}")
    overall = summary.get("overall", {})
    lines += [
        "",
        "| Split | n | JSON valid | Accuracy | Mean evidence items |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| overall | {overall.get('n', 0)} | {overall.get('json_valid_rate', 0):.4f} | {overall.get('accuracy', 0):.4f} | {overall.get('mean_evidence_items', 0):.4f} |",
    ]
    for track, row in summary.get("by_track", {}).items():
        lines.append(f"| {track} | {row.get('n', 0)} | {row.get('json_valid_rate', 0):.4f} | {row.get('accuracy', 0):.4f} | {row.get('mean_evidence_items', 0):.4f} |")
    cost = summary.get("cost_estimate_usd") or {}
    if cost.get("input_tokens") is not None:
        lines += [
            "",
            "## Token usage and cost",
            "",
            f"- Input tokens: {cost.get('input_tokens', 0)}",
            f"- Output tokens: {cost.get('output_tokens', 0)}",
        ]
        if "list_price_cost" in cost:
            lines.append(f"- List-price cost: ${cost['list_price_cost']:.4f} (per-M input ${cost['list_price_input_per_m']}, output ${cost['list_price_output_per_m']}, captured {cost.get('captured','?')})")
        if "batch_estimated_cost" in cost:
            lines.append(f"- Batch-discounted estimate: ${cost['batch_estimated_cost']:.4f} (discount {cost.get('batch_discount')})")
        if "note" in cost:
            lines.append(f"- Note: {cost['note']}")
    if "mechreason_breakdown" in summary:
        mb = summary["mechreason_breakdown"]
        lines += [
            "",
            "## MechReason — per-class accuracy",
            "",
            "| Mechanism class | n | correct | accuracy |",
            "| --- | ---: | ---: | ---: |",
        ]
        for cls, v in sorted(mb["by_class"].items()):
            lines.append(f"| {cls} | {v['n']} | {v['correct']} | {v['accuracy']:.4f} |")
        lines += [
            "",
            "## MechReason — subscore rates",
            "",
            "| Subscore | rate |",
            "| --- | ---: |",
        ]
        for k, v in mb["subscore_rates"].items():
            lines.append(f"| {k} | {v:.4f} |")
        lines.append("")
        lines.append(f"Parse/call errors: {mb['parse_or_call_errors']}")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
