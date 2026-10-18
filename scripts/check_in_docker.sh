#!/usr/bin/env bash
# Build the sandbox once, then check translated C files inside it.
# Usage: bash scripts/check_in_docker.sh results/week1/<model>/c
set -e
DIR="${1:?usage: check_in_docker.sh <results dir>}"
docker build -q -t code-migration-sandbox . > /dev/null
docker run --rm \
  --user "$(id -u):$(id -g)" \
  --network none --memory 512m --pids-limit 128 \
  -v "$PWD":/work:rw -w /work \
  code-migration-sandbox python3 scripts/check_c.py "$DIR"
