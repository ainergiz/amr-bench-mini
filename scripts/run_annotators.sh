#!/usr/bin/env bash
# Run AMRFinderPlus + ResFinder on every FASTA missing a corresponding output.
# Designed for the post-scale corpus pull. Parallelism is per-tool to keep
# Docker stable on a laptop.
set -euo pipefail
cd "$(dirname "$0")/.."

PARALLEL_AMRFINDER=4
PARALLEL_RESFINDER=6

mkdir -p outputs/amrfinder outputs/resfinder logs

missing_amrfinder=$(comm -23 <(ls data/fasta/ | sed 's/.fna$//' | sort) <(ls outputs/amrfinder/ 2>/dev/null | sed 's/.tsv$//' | sort))
missing_resfinder=$(comm -23 <(ls data/fasta/ | sed 's/.fna$//' | sort) <(find outputs/resfinder -maxdepth 1 -mindepth 1 -type d 2>/dev/null | xargs -n1 -I{} basename {} | sort))

echo "AMRFinderPlus to run: $(echo "$missing_amrfinder" | wc -l | tr -d ' ')"
echo "ResFinder to run    : $(echo "$missing_resfinder" | wc -l | tr -d ' ')"

run_amrfinder() {
    local gid="$1"
    docker run --rm \
        -v "$(pwd)/data/fasta:/in:ro" \
        -v "$(pwd)/outputs/amrfinder:/out" \
        ncbi/amr:latest \
        amrfinder -n "/in/${gid}.fna" --organism Klebsiella_pneumoniae \
        -o "/out/${gid}.tsv" 2>"logs/amrfinder_${gid}.log"
}

run_resfinder() {
    local gid="$1"
    mkdir -p "outputs/resfinder/${gid}"
    docker run --rm --platform linux/amd64 \
        -v "$(pwd)/data/fasta:/in:ro" \
        -v "$(pwd)/outputs/resfinder/${gid}:/out" \
        genomicepidemiology/resfinder:latest \
        --acquired --inputfasta "/in/${gid}.fna" -o /out 2>"logs/resfinder_${gid}.log"
}

export -f run_amrfinder run_resfinder

if [[ -n "$missing_amrfinder" ]]; then
    echo "Starting AMRFinderPlus jobs ..."
    echo "$missing_amrfinder" | xargs -n 1 -P "$PARALLEL_AMRFINDER" -I {} bash -c 'run_amrfinder "$@"' _ {} || true
fi

if [[ -n "$missing_resfinder" ]]; then
    echo "Starting ResFinder jobs ..."
    echo "$missing_resfinder" | xargs -n 1 -P "$PARALLEL_RESFINDER" -I {} bash -c 'run_resfinder "$@"' _ {} || true
fi

echo "AMRFinderPlus outputs: $(ls outputs/amrfinder | wc -l | tr -d ' ')"
echo "ResFinder outputs    : $(find outputs/resfinder -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ')"

# Refresh outputs/provenance.json with current docker image + db versions so the
# AMRFinderPlus TSVs (which do not embed version info) are pinned.
python3 scripts/capture_annotator_provenance.py >/dev/null
echo "Refreshed outputs/provenance.json"
