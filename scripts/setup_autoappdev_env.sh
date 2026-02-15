#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_NAME="autoappdev"
PY_VER="3.11"
REQ_FILE="$ROOT_DIR/backend/requirements.txt"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found on PATH. Install Miniconda/Anaconda first." >&2
  exit 1
fi

export CONDA_NO_PLUGINS=true

if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda install -n "$ENV_NAME" -y "python=$PY_VER" pip
else
  conda create -n "$ENV_NAME" -y "python=$PY_VER" pip
fi

conda run -n "$ENV_NAME" python -m pip install -r "$REQ_FILE"

echo "Conda env ready: $ENV_NAME"

