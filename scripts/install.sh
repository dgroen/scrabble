#!/usr/bin/env bash
set -euo pipefail

# Install project dependencies using uv when available, otherwise create .venv and install

if command -v uv >/dev/null 2>&1; then
  echo "uv detected — trying uv install variants"
  if uv install; then
    echo "uv install succeeded"
    exit 0
  fi

  if uv pip install -r dev-requirements.txt; then
    echo "uv pip install -r dev-requirements.txt succeeded"
    exit 0
  fi

  if uv pip install -e '.[dev]'; then
    echo "uv pip install -e '.[dev]' succeeded"
    exit 0
  fi

  echo "uv present but none of the attempted install commands succeeded; falling back to .venv" >&2
fi

echo "Creating .venv and installing dependencies into it"
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]' || pip install -r dev-requirements.txt

echo "Installation complete. Activate with: source .venv/bin/activate"
