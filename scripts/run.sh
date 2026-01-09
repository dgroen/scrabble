#!/usr/bin/env bash
set -euo pipefail

# Run a command inside the project's virtualenv.
# If `uv` is available it uses `uv run ...`, otherwise it activates `.venv`.

if command -v uv >/dev/null 2>&1; then
  exec uv run "$@"
fi

if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
  exec "$@"
else
  echo "No uv found and .venv is missing. Create venv with './scripts/install.sh' or 'make venv'." >&2
  exit 2
fi
