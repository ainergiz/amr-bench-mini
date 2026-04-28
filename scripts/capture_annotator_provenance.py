#!/usr/bin/env python3
"""Capture AMRFinderPlus + ResFinder tool/db versions and image digests.

Probes the docker images currently used by scripts/run_annotators.sh and writes
``outputs/provenance.json`` with:
    - tool name and version
    - database version
    - docker image RepoDigest (preferred) and config Id
    - capture date

This script is idempotent. Re-run it whenever the docker images are pulled/updated.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "provenance.json"


def docker_or_die() -> None:
    if not shutil.which("docker"):
        raise SystemExit("docker not found in PATH; cannot probe annotator versions.")


def capture_amrfinder() -> dict:
    out = subprocess.run(
        ["docker", "run", "--rm", "ncbi/amr:latest", "amrfinder", "-V"],
        capture_output=True, text=True, check=False,
    )
    text = out.stdout + out.stderr
    sw = re.search(r"Software version:\s*(\S+)", text)
    db = re.search(r"Database version:\s*(\S+)", text)
    image = capture_image_digests("ncbi/amr:latest")
    return {
        "tool": "AMRFinderPlus",
        "tool_version": sw.group(1) if sw else None,
        "database_version": db.group(1) if db else None,
        "docker_image": "ncbi/amr:latest",
        **image,
        "raw_version_output": text.strip(),
    }


def capture_resfinder() -> dict:
    # ResFinder embeds db version and command params in each per-genome JSON,
    # so prefer that. Fall back to image digest lookup only.
    db_version = None
    sample = next(ROOT.glob("outputs/resfinder/*/573.json"), None)
    if sample:
        try:
            data = json.loads(sample.read_text())
            for key, info in (data.get("databases") or {}).items():
                if info.get("database_name") == "ResFinder":
                    db_version = info.get("database_version")
                    break
        except (OSError, json.JSONDecodeError):
            pass
    image = capture_image_digests("genomicepidemiology/resfinder:latest")
    return {
        "tool": "ResFinder",
        "tool_version_note": "Per-run software command and parameters are recorded in outputs/resfinder/<genome>/573.json under software_executions.",
        "database_version": db_version,
        "docker_image": "genomicepidemiology/resfinder:latest",
        **image,
        "sample_json": str(sample.relative_to(ROOT)) if sample else None,
    }


def capture_image_digests(image: str) -> dict:
    info: dict[str, str | None] = {"repo_digest": None, "image_id": None}
    for fmt, key in (("{{index .RepoDigests 0}}", "repo_digest"), ("{{.Id}}", "image_id")):
        try:
            out = subprocess.run(
                ["docker", "inspect", f"--format={fmt}", image],
                capture_output=True, text=True, check=False,
            )
            value = out.stdout.strip()
            if value and "no value" not in value.lower():
                info[key] = value
        except FileNotFoundError:
            return info
    return info


def main() -> None:
    docker_or_die()
    provenance = {
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "captured_host": subprocess.run(
            ["uname", "-srm"], capture_output=True, text=True, check=False
        ).stdout.strip(),
        "annotators": {
            "amrfinder": capture_amrfinder(),
            "resfinder": capture_resfinder(),
        },
        "notes": (
            "AMRFinderPlus TSV outputs do not embed version info; this provenance file is the "
            "authoritative version pin for outputs/amrfinder/. ResFinder embeds full software/db "
            "provenance in each outputs/resfinder/<genome>/573.json."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(provenance, indent=2, sort_keys=True))
    print(f"Wrote {OUT}")
    print(json.dumps(provenance, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
