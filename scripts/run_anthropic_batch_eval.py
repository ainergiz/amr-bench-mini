#!/usr/bin/env python3
"""Run MechReason eval through Anthropic Message Batches.

This is the discounted/asynchronous companion to ``run_llm_eval.py``. It
submits all selected tasks as one Anthropic Message Batch, polls until the
batch ends, then writes the same core artifacts:

    raw_outputs.jsonl
    summary.json
    summary.md
    manifest.json
    prompts.txt
    tasks_used.jsonl
    dataset_summary_snapshot.json

Usage:
    python3 scripts/run_anthropic_batch_eval.py --pilot --model claude-opus-4-7
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from amr_bench.agent import build_messages, parse_json_response  # noqa: E402
from amr_bench.io import read_jsonl, write_json, write_jsonl  # noqa: E402
from amr_bench.pricing import cost_estimate as pricing_cost_estimate  # noqa: E402
from amr_bench.scoring import aggregate_scores, score_output  # noqa: E402
from run_llm_eval import mechreason_breakdown, render_summary_md, write_manifest  # noqa: E402

TASKS = ROOT / "data" / "tasks"
RESULTS = ROOT / "results" / "llm_eval"


def main() -> None:
    args = parse_args()
    load_dotenv_local()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY env var not set; .env.local was also missing it")

    try:
        import anthropic  # type: ignore
    except ImportError as exc:
        raise SystemExit("anthropic SDK not installed; use .venv/bin/python or install anthropic") from exc

    tasks, source_path = load_tasks(args)
    run_name = args.run_name or default_run_name(args)
    out_dir = RESULTS / run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_args = argparse.Namespace(
        smoke=False,
        pilot=args.pilot,
        tasks_file=args.tasks_file,
        limit=args.limit,
        provider="anthropic_batch",
        model=args.model,
        max_tokens=args.max_tokens,
        save_raw=args.save_raw,
    )
    write_manifest(out_dir, manifest_args, tasks, source_path, run_name)

    print(f"Loaded {len(tasks)} tasks from {describe_source(args)}")
    print(f"Output directory: {out_dir}")
    print(f"Submitting Anthropic Message Batch: model={args.model}, max_tokens={args.max_tokens}")

    client = anthropic.Anthropic()
    requests = [make_batch_request(task, args.model, args.max_tokens) for task in tasks]
    submitted_at = time.time()
    batch = client.messages.batches.create(requests=requests)
    write_json(out_dir / "batch_submission.json", to_jsonable(batch))
    print(f"Batch submitted: {batch.id}")

    status_history = []
    while True:
        current = client.messages.batches.retrieve(batch.id)
        status = to_jsonable(current)
        status_history.append({"checked_at_utc": datetime.now(timezone.utc).isoformat(), "batch": status})
        write_json(out_dir / "batch_status_history.json", status_history)

        counts = getattr(current, "request_counts", None)
        counts_text = ""
        if counts is not None:
            counts_text = (
                f" processing={counts.processing}"
                f" succeeded={counts.succeeded}"
                f" errored={counts.errored}"
                f" canceled={counts.canceled}"
                f" expired={counts.expired}"
            )
        elapsed = time.time() - submitted_at
        print(f"[{elapsed:6.1f}s] status={current.processing_status}{counts_text}", flush=True)

        if current.processing_status == "ended":
            batch = current
            break
        if elapsed > args.timeout_minutes * 60:
            raise SystemExit(f"Timed out waiting for batch {batch.id}; artifacts are in {out_dir}")
        time.sleep(args.poll_interval)

    rows, scored, usage_totals = collect_results(client, batch.id, tasks, args, time.time() - submitted_at)

    summary = aggregate_scores(scored)
    summary["run_name"] = run_name
    summary["provider"] = "anthropic_batch"
    summary["model"] = args.model
    summary["n_tasks"] = len(tasks)
    summary["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    summary["batch_id"] = batch.id
    summary["batch_elapsed_s"] = round(time.time() - submitted_at, 3)
    summary["batch_status"] = to_jsonable(batch)
    summary["usage_totals"] = dict(usage_totals)
    summary["cost_estimate_usd"] = cost_estimate(usage_totals, args.model)

    if any(t["track"] == "mechreason" for t in tasks):
        summary["mechreason_breakdown"] = mechreason_breakdown(rows)

    write_jsonl(out_dir / "raw_outputs.jsonl", rows)
    write_json(out_dir / "summary.json", summary)
    summary_md = render_summary_md(summary) + render_batch_cost_md(summary)
    (out_dir / "summary.md").write_text(summary_md)

    print()
    print(summary_md)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--pilot", action="store_true", help="Use data/tasks/mechreason_pilot.jsonl.")
    src.add_argument("--tasks-file", type=Path, help="JSONL of tasks to run.")
    p.add_argument("--limit", type=int, default=None, help="Cap tasks after loading.")
    p.add_argument("--model", default="claude-opus-4-7")
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--run-name", default=None)
    p.add_argument("--save-raw", action="store_true")
    p.add_argument("--poll-interval", type=float, default=30.0)
    p.add_argument("--timeout-minutes", type=float, default=120.0)
    return p.parse_args()


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


def load_tasks(args: argparse.Namespace) -> tuple[list[dict], Path]:
    path = TASKS / "mechreason_pilot.jsonl" if args.pilot else args.tasks_file
    if not path or not path.exists():
        raise SystemExit(f"Tasks file not found: {path}")
    tasks = read_jsonl(path)
    if args.limit:
        tasks = tasks[: args.limit]
    return tasks, path


def describe_source(args: argparse.Namespace) -> str:
    return "data/tasks/mechreason_pilot.jsonl" if args.pilot else str(args.tasks_file)


def default_run_name(args: argparse.Namespace) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short = args.model.replace("/", "-").replace(":", "-")
    prefix = "pilot_batch" if args.pilot else "adhoc_batch"
    return f"{prefix}_{short}_{stamp}"


def make_batch_request(task: dict[str, Any], model: str, max_tokens: int) -> dict[str, Any]:
    messages = build_messages(task, scaffolded=True)
    system = next((m["content"] for m in messages if m["role"] == "system"), "")
    user_msgs = [m for m in messages if m["role"] != "system"]
    return {
        "custom_id": task["task_id"],
        "params": {
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": m["role"], "content": m["content"]} for m in user_msgs],
        },
    }


def collect_results(client: Any, batch_id: str, tasks: list[dict], args: argparse.Namespace, elapsed_s: float):
    tasks_by_id = {t["task_id"]: t for t in tasks}
    results_by_id: dict[str, Any] = {}
    for item in client.messages.batches.results(batch_id):
        results_by_id[item.custom_id] = item

    rows = []
    scored = []
    usage_totals: dict[str, int] = defaultdict(int)

    for task in tasks:
        item = results_by_id.get(task["task_id"])
        raw = ""
        usage: dict[str, int] = {}
        result_type = "missing"
        if item is None:
            parsed = {"task_id": task["task_id"], "__call_error": "missing batch result"}
        else:
            result = item.result
            result_type = getattr(result, "type", "unknown")
            if result_type == "succeeded":
                message = result.message
                raw = "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
                parsed = parse_json_response(raw)
                if "task_id" not in parsed:
                    parsed["task_id"] = task["task_id"]
                usage = extract_anthropic_usage(message)
            else:
                parsed = {"task_id": task["task_id"], "__call_error": json.dumps(to_jsonable(result))}

        for key, value in usage.items():
            if isinstance(value, int):
                usage_totals[key] += value
        score = score_output(task, parsed)
        rows.append(
            {
                "task_id": task["task_id"],
                "track": task["track"],
                "task": task,
                "gold": task["gold"],
                "model": args.model,
                "provider": "anthropic_batch",
                "batch_result_type": result_type,
                "output": parsed,
                "raw_response": raw if args.save_raw else None,
                "score": score,
                "latency_s": None,
                "batch_elapsed_s": round(elapsed_s, 3),
                "usage": usage,
            }
        )
        scored.append(score)

    return rows, scored, usage_totals


def extract_anthropic_usage(message: Any) -> dict[str, int]:
    usage_obj = getattr(message, "usage", None)
    if usage_obj is None:
        return {}
    usage = {}
    for key in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"):
        value = getattr(usage_obj, key, None)
        if value is not None:
            usage[key] = int(value)
    return usage


def cost_estimate(usage_totals: dict[str, int], model: str) -> dict[str, float]:
    return pricing_cost_estimate(model, "anthropic", usage_totals, is_batch=True)


def render_batch_cost_md(summary: dict[str, Any]) -> str:
    cost = summary.get("cost_estimate_usd", {})
    if not cost:
        return ""
    return (
        "\n\n## Anthropic batch cost estimate\n\n"
        f"- Batch ID: `{summary.get('batch_id')}`\n"
        f"- Elapsed: {summary.get('batch_elapsed_s')}s\n"
        f"- Input tokens: {cost.get('input_tokens', 0)}\n"
        f"- Output tokens: {cost.get('output_tokens', 0)}\n"
        f"- List-price cost: ${cost.get('list_price_cost', 0):.4f}\n"
        f"- Batch estimated cost: **${cost.get('batch_estimated_cost', 0):.4f}**\n"
    )


def to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_jsonable(v) for v in obj]
    return obj


if __name__ == "__main__":
    main()
