# Installing & Running vLLM

A guide to installing [vLLM](https://docs.vllm.ai/) on this machine and serving
models through its OpenAI-compatible API.

## Hardware

| Component | Detail |
|-----------|--------|
| OS | Ubuntu 24.04 LTS |
| RAM | 128 GB |
| GPU | NVIDIA Quadro P620 (2 GB VRAM — Pascal / GP107) |

---

## ⚠️ Important: GPU Compatibility

vLLM's CUDA backend **requires NVIDIA compute capability 7.0 or higher**
(Volta, Turing, Ampere, Ada, Hopper, …).

The **Quadro P620 is Pascal (GP107), compute capability 6.1**, so it is
**not supported** by vLLM's GPU path. Even if it were, 2 GB of VRAM is far too
small to load a useful model.

> **Bottom line:** on this machine you should run the **vLLM CPU backend**,
> which uses system RAM (128 GB here — plenty) instead of the GPU.
>
> If you only want the simplest local-inference experience, **Ollama** or
> **llama-cpp-python** (see `README.md`) are better suited to a Pascal + low-VRAM
> setup. Use vLLM here mainly if you specifically need its OpenAI-compatible
> server, continuous batching, or want to prototype against the vLLM API.

---

## Option A — vLLM CPU Backend (recommended for this machine)

The CPU backend is not published as a regular wheel; it is built from source.

### 1. System prerequisites

```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    g++ \
    git \
    python3-dev \
    libnuma-dev \
    numactl
```

> A recent compiler with **AVX2** (or AVX-512) support is recommended. Check
> with `lscpu | grep -o 'avx[0-9_]*' | sort -u`.

### 2. Python environment

```bash
cd /home/loum/projects/LocalLLMAgent
python3 -m venv .venv-vllm
source .venv-vllm/bin/activate
pip install --upgrade pip setuptools wheel
```

### 3. Build vLLM for CPU

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm

# Install Python build/runtime requirements for the CPU target
pip install -r requirements/cpu.txt

# Build and install vLLM with the CPU backend
VLLM_TARGET_DEVICE=cpu pip install -e . --no-build-isolation
```

> The build can take several minutes as it compiles native extensions.
> If `requirements/cpu.txt` does not exist on your checked-out version, look for
> `requirements-cpu.txt` in the repo root instead.

### 4. Useful CPU runtime environment variables

```bash
# Amount of RAM (GiB) vLLM may use for the KV cache per process
export VLLM_CPU_KVCACHE_SPACE=40

# Pin worker threads to physical CPU cores (improves throughput)
export VLLM_CPU_OMP_THREADS_BIND=auto
```

### 5. Serve a model (OpenAI-compatible API)

Pick a **small, quantised or 1–8B** model — CPU inference is memory-bandwidth
bound and gets slow quickly with larger models.

```bash
vllm serve Qwen/Qwen2.5-1.5B-Instruct \
    --device cpu \
    --dtype bfloat16 \
    --max-model-len 4096
```

The server listens on `http://localhost:8000/v1` by default.

---

## Option B — vLLM GPU Backend (NOT usable on the P620)

Documented here only for reference / a future GPU upgrade
(needs a compute-capability ≥ 7.0 card with adequate VRAM).

```bash
python3 -m venv .venv-vllm
source .venv-vllm/bin/activate
pip install --upgrade pip

# Standard CUDA wheel (compute capability >= 7.0 required)
pip install vllm

vllm serve meta-llama/Llama-3.2-3B-Instruct \
    --dtype auto \
    --max-model-len 8192
```

This will **fail** on the Quadro P620 with an "unsupported GPU / compute
capability too low" style error — expected, given the Pascal architecture.

---

## Testing the Server

Once `vllm serve` is running, it exposes the OpenAI API on port `8000`.

### curl

```bash
# List models
curl http://localhost:8000/v1/models

# Chat completion
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2.5-1.5B-Instruct",
        "messages": [{"role": "user", "content": "Explain vLLM in one sentence."}]
    }'
```

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",  # vLLM ignores the key by default
)

resp = client.chat.completions.create(
    model="Qwen/Qwen2.5-1.5B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(resp.choices[0].message.content)
```

---

## Common `vllm serve` Flags

| Flag | Purpose |
|------|---------|
| `--device cpu` | Force the CPU backend |
| `--dtype bfloat16` | Data type (`bfloat16` works well on modern CPUs) |
| `--max-model-len 4096` | Maximum context length (lower = less RAM) |
| `--host 0.0.0.0` | Bind to all interfaces |
| `--port 8000` | API port |
| `--api-key <key>` | Require an API key |
| `--gpu-memory-utilization` | (GPU only) fraction of VRAM to use |

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---------|--------------------|
| `RuntimeError: ... compute capability` | GPU too old (Pascal). Use `--device cpu`. |
| Build fails on native extension | Install `build-essential cmake g++ python3-dev`; ensure venv is active. |
| Very slow generation | Expected on CPU — use a small model, lower `--max-model-len`, set `VLLM_CPU_OMP_THREADS_BIND`. |
| OOM / killed | Lower `VLLM_CPU_KVCACHE_SPACE`, `--max-model-len`, or pick a smaller model. |
| `requirements/cpu.txt` not found | Use `requirements-cpu.txt` (older layouts) or check the repo's `requirements/` dir. |

---

## References

- vLLM docs: https://docs.vllm.ai/
- CPU installation: https://docs.vllm.ai/en/latest/getting_started/installation/cpu.html
- Supported hardware: https://docs.vllm.ai/en/latest/getting_started/installation.html
