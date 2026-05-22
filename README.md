# LocalLLM

Host and interact with large language models entirely on your own hardware.

## Hardware

| Component | Detail |
|-----------|--------|
| OS | Ubuntu 24.04 LTS |
| RAM | 128 GB |
| GPU | NVIDIA Quadro P620 (2 GB VRAM — Pascal / GP107) |

> **VRAM note:** Most inference runs on CPU/RAM. With 128 GB RAM, quantised models up to ~70B parameters are feasible. The P620 can accelerate a handful of transformer layers via partial offloading when using `llama-cpp-python`.

---

## Quick Start

### 1. Prerequisites

```bash
# NVIDIA userspace utilities + CUDA toolkit
sudo apt-get install -y nvidia-utils-580 nvidia-cuda-toolkit

# Verify GPU is visible
nvidia-smi
```

### 2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
```

### 3. Pull models

```bash
ollama pull llama3.2:3b        # 2 GB — fast, lightweight
ollama pull gemma4:27b         # ~16 GB — high quality MoE (4B active params)
ollama pull nomic-embed-text   # 274 MB — embeddings for RAG
```

### 4. Python environment

```bash
cd /home/loum/projects/LocalLLM
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies with uv (faster, modern Python package manager)
uv pip install -r requirements.txt

# Optional: llama-cpp-python with CUDA support
CMAKE_ARGS="-DGGML_CUDA=on" uv pip install llama-cpp-python --no-cache-dir
```

---

## Project Structure

```
LocalLLM/
├── .venv/                        Python virtual environment
├── requirements.txt              Python dependencies
├── data/
│   └── chroma_db/                Persistent ChromaDB vector store (auto-created)
├── examples/
│   ├── 01_basic_chat.py          Synchronous + multi-turn chat via Ollama client
│   ├── 02_streaming.py           Token-by-token streaming (native + OpenAI compat)
│   ├── 03_rag_chromadb.py        RAG pipeline: embed → store → retrieve → answer
│   ├── 04_code_generation.py     Code generation, explanation, and review
│   └── 05_openai_compat_api.py   OpenAI SDK drop-in, structured output, tool calls
└── README.md
```

---

## Running the Examples

```bash
source .venv/bin/activate

# Make sure Ollama is serving
ollama serve &   # or: sudo systemctl start ollama

python examples/01_basic_chat.py
python examples/02_streaming.py
python examples/03_rag_chromadb.py   # requires: ollama pull nomic-embed-text
python examples/04_code_generation.py
python examples/05_openai_compat_api.py
```

---

## Ollama Cheat Sheet

```bash
ollama list                    # show downloaded models
ollama pull <model>            # download a model
ollama rm <model>              # remove a model
ollama run <model>             # interactive CLI chat
ollama ps                      # show currently loaded models

# API (runs on port 11434 by default)
curl http://localhost:11434/api/tags           # list models
curl http://localhost:11434/v1/models          # OpenAI-compat model list
```

---

## Recommended Models

| Model | Size (Q4) | Best For |
|-------|-----------|----------|
| `llama3.2:3b` | 2 GB | Fast chat, prototyping |
| `llama3.1:8b` | 5 GB | General purpose |
| `gemma4:27b` | ~16 GB | High quality, MoE efficiency |
| `qwen2.5:7b` | 5 GB | Code + multilingual |
| `deepseek-coder-v2:16b` | 10 GB | Code generation |
| `nomic-embed-text` | 274 MB | Embeddings / RAG |

---

## Partial GPU Offloading (llama-cpp-python)

With 2 GB VRAM you can offload ~6–10 transformer layers to the GPU, accelerating prefill:

```python
from llama_cpp import Llama

llm = Llama(
    model_path="path/to/model.gguf",
    n_gpu_layers=8,   # adjust; higher = more VRAM used
    n_ctx=4096,
)
response = llm("Explain RAG in one paragraph.", max_tokens=256)
print(response["choices"][0]["text"])
```
