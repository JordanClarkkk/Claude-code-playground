#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_DIR="$BACKEND_DIR/venv"

# Find python3 or python
if command -v python3 &>/dev/null; then
  PY=python3
elif command -v python &>/dev/null; then
  PY=python
else
  echo "Error: Python is not installed. Install Python 3.10+ and try again."
  exit 1
fi

echo "Using: $($PY --version)"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  $PY -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing dependencies..."
pip install -q -r "$BACKEND_DIR/requirements.txt"

# Start server
echo ""
echo "=========================================="
echo "  Open http://localhost:8000 in your browser"
echo "=========================================="
echo ""

cd "$BACKEND_DIR"
python -m uvicorn main:app --host 0.0.0.0 --port 8000
