#!/usr/bin/env python3
"""Run MechReason eval through the Gemini Batch API.

Mirrors scripts/run_anthropic_batch_eval.py: submits all selected tasks as one
inlined batch job, polls until the job ends, then writes the same core
artifacts so that rescore_runs.py and build_headline_table.py treat the run
identically to a live run.

Usage:
    # Hard split, with substrate context
    python3 scripts/run_gemini_batch_eval.py \\
        --tasks-file data/tasks/mechreason_hard.jsonl \\
        --model gemini-3.1-pro-preview \\
        --card-substrate-context

    # Full corpus (no tool)
    python3 scripts/run_gemini_batch_eval.py \\
        --tasks-file data/tasks/mechreason.jsonl \\
        --model gemini-3.1-pro-preview

The Gemini Developer API supports inlined requests directly. For very large
corpora (1000+) consider switching to a file source via client.files.upload.
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
from run_llm_eval import (  # noqa: E402
    load_dotenv_local,
    mechreason_breakdown,
    render_summary_md,
    write_manifest,
)

TASKS = ROOT / "data" / "tasks"
RESULTS = ROOT / "results" / "llm_eval"
TERMINAL_STATES = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}


def main() -> None:
    args = parse_args()
    load_dotenv_local()

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or GOOGLE_GENERATIVE_AI_API_KEY for the batch runner.")

    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
    except ImportError:
        raise SystemExit("google-genai SDK not installed; uv pip install google-genai")

    tasks, source_path = load_tasks(args)
    print(f"Loaded {len(tasks)} tasks from {describe_source(args)}")

    run_name = args.run_name or default_run_name(args)
    out_dir = RESULTS / run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {out_dir}")

    write_manifest(out_dir, args, tasks, source_path, run_name)

    client = genai.Client(api_key=api_key)
    inlined = build_inlined_requests(args, tasks, types)
    print(f"Submitting {len(inlined)} inlined requests to model {args.model} ...")

    submission_started = time.time()
    job = client.batches.create(
        model=args.model,
        src={"inlined_requests": inlined},
        config=types.CreateBatchJobConfig(display_name=run_name),
    )
    print(f"Batch submitted: {job.name}  state={job.state}")
    write_json(out_dir / "batch_submission.json", {
        "name": job.name,
        "display_name": run_name,
        "state": str(job.state),
        "submitted_utc": datetime.now(timezone.utc).isoformat(),
        "n_requests": len(inlined),
    })

    job = poll_until_done(client, job.name, args.poll_seconds, args.max_wait_seconds, out_dir)
    elapsed = round(time.time() - submission_started, 1)

    final_state = str(job.state)
    if final_state != "JobState.JOB_STATE_SUCCEEDED":
        write_json(out_dir / "batch_failure.json", {
            "name": job.name,
            "state": final_state,
            "error": getattr(job, "error", None) and job.error.model_dump(mode="json"),
        })
        raise SystemExit(f"Batch ended in non-success state: {final_state}")

    rows, usage_totals = collect_results(args, tasks, job)
    write_jsonl(out_dir / "raw_outputs.jsonl", rows)

    scored = [r["score"] for r in rows]
    summary = aggregate_scores(scored)
    summary.update({
        "run_name": run_name,
        "provider": "gemini_batch",
        "model": args.model,
        "n_tasks": len(tasks),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "usage_totals": dict(usage_totals),
        "batch_id": job.name,
        "batch_elapsed_s": elapsed,
        "card_substrate_context": args.card_substrate_context,
    })
    summary["cost_estimate_usd"] = pricing_cost_estimate(args.model, "gemini_batch", dict(usage_totals), is_batch=True)

    if any(t["track"] == "mechreason" for t in tasks):
        summary["mechreason_breakdown"] = mechreason_breakdown(rows)

    write_json(out_dir / "summary.json", summary)
    md = render_summary_md(summary) + render_batch_cost_md(summary)
    (out_dir / "summary.md").write_text(md)

    print()
    print(md)


# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--pilot", action="store_true", help="Use the frozen 50-task pilot subset.")
    src.add_argument("--tasks-file", type=Path, help="JSONL of tasks to run.")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--model", default="gemini-3.1-pro-preview")
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--run-name", default=None)
    p.add_argument(
        "--card-substrate-context",
        action="store_true",
        help="Inject pre-resolved CARD ARO substrate annotations per visible gene into each prompt.",
    )
    p.add_argument("--poll-seconds", type=int, default=30, help="Polling interval while waiting for the batch.")
    p.add_argument("--max-wait-seconds", type=int, default=24 * 3600, help="Hard ceiling on total wait time.")
    args = p.parse_args()
    args.smoke = False
    args.save_raw = False
    args.provider = "gemini_batch"
    return args


def load_tasks(args: argparse.Namespace) -> tuple[list[dict], Path]:
    path = TASKS / "mechreason_pilot.jsonl" if args.pilot else args.tasks_file
    if not path or not path.exists():
        raise SystemExit(f"Tasks file not found: {path}")
    tasks = read_jsonl(path)
    if args.limit:
        tasks = tasks[: args.limit]
    return tasks, path


def describe_source(args: argparse.Namespace) -> str:
    if args.pilot:
        return "data/tasks/mechreason_pilot.jsonl"
    return str(args.tasks_file)


def default_run_name(args: argparse.Namespace) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short = args.model.replace("/", "-").replace(":", "-")
    if args.pilot:
        return f"pilot_batch_{short}_{stamp}"
    suffix = "_tool" if args.card_substrate_context else ""
    return f"batch{suffix}_{short}_{stamp}"


def build_inlined_requests(args, tasks: list[dict], types_mod) -> list[dict]:
    """Build one InlinedRequest dict per task with metadata.task_id for round-trip."""
    inlined = []
    for task in tasks:
        messages = build_messages(task, scaffolded=True, card_substrate_context=args.card_substrate_context)
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]
        contents = [
            {"role": ("model" if m["role"] == "assistant" else "user"), "parts": [{"text": m["content"]}]}
            for m in user_msgs
        ]
        config = types_mod.GenerateContentConfig(
            system_instruction=system or None,
            max_output_tokens=args.max_tokens,
        )
        inlined.append({
            "contents": contents,
            "config": config,
            "metadata": {"task_id": task["task_id"]},
        })
    return inlined


def poll_until_done(client, name: str, interval: int, max_wait: int, out_dir: Path):
    history: list[dict] = []
    started = time.time()
    while True:
        job = client.batches.get(name=name)
        history.append({
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "state": str(job.state),
            "elapsed_s": round(time.time() - started, 1),
        })
        write_json(out_dir / "batch_status_history.json", {"name": name, "history": history})
        state_str = str(job.state).split(".")[-1]
        print(f"  state={state_str}  elapsed={history[-1]['elapsed_s']}s")
        if state_str in TERMINAL_STATES or getattr(job, "done", False):
            return job
        if time.time() - started > max_wait:
            raise SystemExit(f"Exceeded max wait of {max_wait}s; last state={state_str}")
        time.sleep(interval)


def collect_results(args, tasks: list[dict], job) -> tuple[list[dict], dict]:
    """Walk inlined responses, parse JSON, score, build per-task rows."""
    by_task = {t["task_id"]: t for t in tasks}
    inlined_responses = list(getattr(job.dest, "inlined_responses", []) or [])

    rows: list[dict] = []
    usage_totals: dict[str, int] = defaultdict(int)

    for ir in inlined_responses:
        meta = getattr(ir, "metadata", None) or {}
        tid = meta.get("task_id")
        if not tid or tid not in by_task:
            continue
        task = by_task[tid]
        resp = getattr(ir, "response", None)
        err = getattr(ir, "error", None)
        text = ""
        usage: dict[str, int] = {}
        if err is not None:
            parsed = {"task_id": tid, "__call_error": getattr(err, "message", str(err))}
        elif resp is not None:
            text = getattr(resp, "text", "") or ""
            parsed = parse_json_response(text)
            if "task_id" not in parsed:
                parsed["task_id"] = tid
            meta_usage = getattr(resp, "usage_metadata", None)
            if meta_usage is not None:
                u = {
                    "input_tokens": getattr(meta_usage, "prompt_token_count", None),
                    "output_tokens": getattr(meta_usage, "candidates_token_count", None),
                    "total_tokens": getattr(meta_usage, "total_token_count", None),
                }
                thoughts = getattr(meta_usage, "thoughts_token_count", None)
                if thoughts is not None:
                    u["reasoning_tokens"] = thoughts
                usage = {k: v for k, v in u.items() if v is not None}
        else:
            parsed = {"task_id": tid, "__call_error": "no response and no error"}

        for k, v in usage.items():
            if isinstance(v, (int, float)):
                usage_totals[k] += int(v)

        score = score_output(task, parsed)
        rows.append({
            "task_id": tid,
            "track": task["track"],
            "task": task,
            "gold": task["gold"],
            "model": args.model,
            "provider": "gemini_batch",
            "output": parsed,
            "raw_response": None,
            "score": score,
            "latency_s": None,
            "usage": usage,
        })

    # Preserve task ordering for downstream tools.
    order = {t["task_id"]: i for i, t in enumerate(tasks)}
    rows.sort(key=lambda r: order.get(r["task_id"], 1_000_000))

    seen = {r["task_id"] for r in rows}
    missing = [t["task_id"] for t in tasks if t["task_id"] not in seen]
    if missing:
        print(f"  [warn] {len(missing)} tasks missing from batch results (first 5: {missing[:5]})")
    return rows, usage_totals


def render_batch_cost_md(summary: dict[str, Any]) -> str:
    cost = summary.get("cost_estimate_usd", {})
    if not cost:
        return ""
    pieces = [
        "\n\n## Gemini batch metadata\n",
        f"- Batch ID: `{summary.get('batch_id')}`",
        f"- Elapsed: {summary.get('batch_elapsed_s')}s",
        f"- Input tokens: {cost.get('input_tokens', 0)}",
        f"- Output tokens: {cost.get('output_tokens', 0)}",
    ]
    if "list_price_cost" in cost:
        pieces.append(f"- List-price cost: ${cost['list_price_cost']:.4f}")
    if "batch_estimated_cost" in cost:
        pieces.append(f"- Batch-discounted estimate: ${cost['batch_estimated_cost']:.4f}")
    if "note" in cost:
        pieces.append(f"- Note: {cost['note']}")
    return "\n".join(pieces) + "\n"


if __name__ == "__main__":
    main()
