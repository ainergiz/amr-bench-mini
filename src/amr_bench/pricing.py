"""Per-model price tables and cost estimation for LLM eval runs.

Prices are list prices in USD per 1M tokens, captured from each provider's
public pricing page. Update both the value and the ``captured`` date when
prices change. Models not in the table return a usage-only cost record so
runs still complete; the caller can patch the table via the
``AMR_BENCH_PRICING_OVERRIDES`` env var (path to a JSON file with the same
shape) when needed.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

PRICE_TABLE: dict[str, dict] = {
    # Anthropic — list prices per million tokens.
    "claude-opus-4-7": {
        "provider": "anthropic",
        "input_per_m": 5.0,
        "output_per_m": 25.0,
        "supports_batch_discount": True,
        "batch_discount": 0.5,
        "captured": "2026-04",
    },
    "claude-sonnet-4-6": {
        "provider": "anthropic",
        "input_per_m": 3.0,
        "output_per_m": 15.0,
        "supports_batch_discount": True,
        "batch_discount": 0.5,
        "captured": "2026-04",
    },
    "claude-haiku-4-5-20251001": {
        "provider": "anthropic",
        "input_per_m": 1.0,
        "output_per_m": 5.0,
        "supports_batch_discount": True,
        "batch_discount": 0.5,
        "captured": "2026-04",
    },
}


def _load_overrides() -> dict[str, dict]:
    path = os.environ.get("AMR_BENCH_PRICING_OVERRIDES")
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def lookup(model: str) -> dict | None:
    """Return the price entry for ``model``, applying override JSON if present."""
    overrides = _load_overrides()
    if model in overrides:
        return overrides[model]
    return PRICE_TABLE.get(model)


def cost_estimate(
    model: str,
    provider: str,
    usage_totals: dict[str, int],
    *,
    is_batch: bool = False,
) -> dict:
    input_tokens = int(usage_totals.get("input_tokens", 0) or 0)
    output_tokens = int(usage_totals.get("output_tokens", 0) or 0)
    base = {
        "model": model,
        "provider": provider,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }
    entry = lookup(model)
    if not entry:
        base["note"] = (
            "No price table entry for this model. Set AMR_BENCH_PRICING_OVERRIDES "
            "to a JSON file with the same shape as PRICE_TABLE to attach a price."
        )
        return base

    input_per_m = float(entry["input_per_m"])
    output_per_m = float(entry["output_per_m"])
    list_cost = (input_tokens / 1_000_000) * input_per_m + (output_tokens / 1_000_000) * output_per_m

    base.update(
        {
            "list_price_input_per_m": input_per_m,
            "list_price_output_per_m": output_per_m,
            "list_price_cost": round(list_cost, 6),
            "captured": entry.get("captured"),
        }
    )

    if is_batch and entry.get("supports_batch_discount"):
        discount = float(entry.get("batch_discount", 0.5))
        base["batch_discount"] = discount
        base["batch_estimated_cost"] = round(list_cost * discount, 6)

    return base


@dataclass
class PriceMissing:
    """Indicator value used by callers that want to log when a price is missing."""

    model: str
    provider: str

    def as_record(self) -> dict:
        return {
            "model": self.model,
            "provider": self.provider,
            "note": "No price table entry; cost estimate skipped.",
        }
