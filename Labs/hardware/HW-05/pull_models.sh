#!/usr/bin/env bash
# pull_models.sh - download the language models of Day 10
#
# Run on: the Raspberry Pi 5 (the master card), after setup_pi.sh of HW-04.
# Use:    bash pull_models.sh           the two models of Part A and Part B
#         bash pull_models.sh extras    also the models for Part C
#
# Download sizes (Ollama library, read on 2026-10-01):
#   llama3.2:1b        1.32 GB
#   llama3.2:3b        2.02 GB
#   nomic-embed-text   0.27 GB   (extras: retrieval-augmented generation)
#   llava-phi3:3.8b    2.93 GB   (extras: image description)
set -euo pipefail

MODELS=(llama3.2:1b llama3.2:3b)
if [ "${1:-}" = "extras" ]; then
    MODELS+=(nomic-embed-text llava-phi3:3.8b)
fi

if ! command -v ollama >/dev/null 2>&1; then
    echo "ERROR: ollama not found. Run setup_pi.sh of HW-04 first."
    exit 1
fi

for model in "${MODELS[@]}"; do
    echo "=== ollama pull $model ==="
    ollama pull "$model"
done

echo
ollama list
