#!/usr/bin/env bash
set -euo pipefail

PYTHON="${PYTHON:-python3}"
VENV_DIR=".venv"

echo "==> Checking Python"
"${PYTHON}" --version

echo "==> Creating virtual environment"
"${PYTHON}" -m venv "${VENV_DIR}"

source "${VENV_DIR}/bin/activate"

echo "==> Upgrading packaging tools"
python -m pip install --upgrade pip setuptools wheel

if [[ -f requirements.txt ]]; then
    echo "==> Installing Python dependencies"
    python -m pip install -r requirements.txt
fi

echo "==> Environment ready"
python --version
pip --version

echo
echo "Activate with:"
echo "source ${VENV_DIR}/bin/activate"
