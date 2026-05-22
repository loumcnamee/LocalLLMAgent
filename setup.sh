#!/usr/bin/env bash
# setup.sh — One-shot project setup script
# Run from the project root after cloning / first checkout.
# Usage: bash setup.sh

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$PROJECT_DIR/.venv"

echo "==> Activating virtual environment …"
# shellcheck source=/dev/null
source "$VENV/bin/activate"


echo "==> Installing Python dependencies with uv …"
uv pip install -r "$PROJECT_DIR/requirements.txt"

echo ""
echo "==> Optional: build llama-cpp-python with CUDA support"
echo "    Run manually if you want partial GPU layer offloading:"
echo "    CMAKE_ARGS=\"-DGGML_CUDA=on\" uv pip install llama-cpp-python --no-cache-dir"
echo ""

echo "==> Checking Ollama …"
if ! command -v ollama &>/dev/null; then
    echo "    Ollama not found. Install with:"
    echo "    curl -fsSL https://ollama.com/install.sh | sh"
else
    echo "    Ollama found: $(ollama --version)"
    echo ""
    echo "==> Pulling models (this may take a while) …"
    ollama pull llama3.2:3b
    ollama pull nomic-embed-text
    echo ""
    echo "    To pull the large Gemma4 27B model:"
    echo "    ollama pull gemma4:27b"
fi

echo ""
echo "==> Setup complete. Activate the venv with:"
echo "    source .venv/bin/activate"
