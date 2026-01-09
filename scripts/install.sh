#!/usr/bin/env bash
set -euo pipefail

# Install project dependencies using uv when available, otherwise create .venv and install

if command -v uv >/dev/null 2>&1; then
  echo "uv detected — running 'uv install'"
  uv install
  exit $?
fi

echo "uv not detected — creating .venv and installing dependencies into it"
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
if python -c "import importlib.util, sys; print(importlib.util.find_spec('setuptools') is not None)" | grep -q True; then
  pip install -e '.[dev]' || pip install -r dev-requirements.txt
else
  pip install -e '.[dev]' || pip install -r dev-requirements.txt
fi

echo "Installation complete. Activate with: source .venv/bin/activate"
