#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_NAME="lightmind_backend"
PY_VER="3.11"
REQ_FILE="$ROOT_DIR/auto-apps/backend/requirements.txt"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found on PATH. Install Miniconda/Anaconda first." >&2
  exit 1
fi

# Codex/non-interactive shells sometimes trigger conda plugin failures
# (e.g., virtual package detection like CUDA). Disable plugins to keep this
# env setup script reliable across environments.
export CONDA_NO_PLUGINS=true

if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda install -n "$ENV_NAME" -y "python=$PY_VER" pip
else
  conda create -n "$ENV_NAME" -y "python=$PY_VER" pip
fi

if [[ -f "$REQ_FILE" ]]; then
  conda run -n "$ENV_NAME" python -m pip install -r "$REQ_FILE"
else
  echo "Backend requirements not found, skipping pip install: $REQ_FILE" >&2
fi

echo "Conda env ready: $ENV_NAME"
