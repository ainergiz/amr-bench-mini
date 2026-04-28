#!/usr/bin/env python3
"""Freeze a balanced ~50-task MechReason pilot subset for the small LLM eval.

Stratification strategy (oversample fragile classes):
  intrinsic                       : 3 (all)
  regulator_loss_of_function      : 2 (all)
  permeability_loss (hybrid)      : all 4 currently tagged
  permeability_loss (non-hybrid)  : 6
  insufficient_evidence           : 8  (HypothesisGen)
  efflux                          : 6
  target_modification             : 7
  enzymatic_inactivation          : 10
  metabolic_bypass                : 4
  ---
  TOTAL                           : ~50 tasks

Output: data/tasks/mechreason_pilot.jsonl with the frozen subset.
The pilot list is deterministic (random seed) so re-running gives the same set.
"""
from __future__ import annotations

import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from amr_bench.io import read_jsonl, write_jsonl  # noqa: E402

TASKS = ROOT / "data" / "tasks"
SEED = 20260425

PILOT_TARGETS: dict[str, int] = {
    "intrinsic": 3,
    "regulator_loss_of_function": 5,        # only 2 available, take all
    "permeability_loss_hybrid": 4,           # take all 4 currently hybrid-tagged
    "permeability_loss_nonhybrid": 6,
    "insufficient_evidence": 8,              # HypothesisGen oversample
    "efflux": 6,
    "target_modification": 7,
    "enzymatic_inactivation": 10,
    "metabolic_bypass": 4,
}


def main() -> None:
    tasks = read_jsonl(TASKS / "mechreason.jsonl")
    if not tasks:
        raise SystemExit("No MechReason tasks found. Run scripts/build_tasks.py first.")

    bucket: dict[str, list[dict]] = defaultdict(list)
    for t in tasks:
        cls = t["gold"]["mechanism_class"]
        if cls == "permeability_loss":
            if t["gold"].get("secondary_mechanism_classes"):
                bucket["permeability_loss_hybrid"].append(t)
            else:
                bucket["permeability_loss_nonhybrid"].append(t)
        else:
            bucket[cls].append(t)

    rng = random.Random(SEED)
    pilot: list[dict] = []
    for stratum, target in PILOT_TARGETS.items():
        pool = bucket.get(stratum, [])
        take = min(target, len(pool))
        sampled = rng.sample(pool, take) if take < len(pool) else list(pool)
        pilot.extend(sampled)
        print(f"  {stratum:35s} target={target:>2}  available={len(pool):>3}  sampled={len(sampled)}")

    pilot.sort(key=lambda t: (t["gold"]["mechanism_class"], t["task_id"]))

    out = TASKS / "mechreason_pilot.jsonl"
    write_jsonl(out, pilot)
    print(f"\nWrote {len(pilot)} pilot tasks -> {out}")
    print("Distribution:")
    counts: dict[str, int] = defaultdict(int)
    for t in pilot:
        cls = t["gold"]["mechanism_class"]
        if t["gold"].get("secondary_mechanism_classes"):
            cls += " (hybrid)"
        counts[cls] += 1
    for cls, n in sorted(counts.items()):
        print(f"  {cls:45s}: {n}")


if __name__ == "__main__":
    main()
