# Plan: `local_llm_options.md` — Local LLM Hosting for C++ Development

A comprehensive on-prem report identifying the best way to host local LLMs for C++ software development, balancing **security/data protection** against **performance/correctness**, tailored to your context: **enterprise / many developers, on-prem network-isolated, NVIDIA GPUs + CPU fallback**. Each hosting option lists all tools and third-party technologies involved.

## Document structure

1. **Executive summary + recommendation** (lead with the answer)
2. **Evaluation criteria** — security, data protection, performance, correctness, ops/governance, C++ fit
3. **Per-option deep dives** (overview, architecture, third-party deps, security, performance, correctness, C++ fit, pros/cons):
   - **vLLM** — high-throughput NVIDIA GPU serving, PagedAttention, OpenAI/Anthropic API, multi-LoRA (Apache-2.0)
   - **llama.cpp / llama-server** — C/C++ GGUF, CPU+GPU hybrid, GBNF grammars, CPU fallback (MIT)
   - **LocalAI** — built-in API-key auth, quotas, RBAC, PII redaction, signed images, distributed mTLS (MIT)
   - **Ollama** — easy ops, offline mode (note: disable cloud features for isolation)
   - **LM Studio / llmster** — headless server deploy (license caveats for enterprise)
   - **Tabby** — self-hosted coding assistant: FIM completion + chat + repo RAG (Rust, on-prem Copilot alt)
   - **Brief**: HF TGI, SGLang, NVIDIA NIM
4. **Comparison matrix** (table across all criteria)
5. **Cross-cutting toolchain**:
   - *Security/data protection*: mTLS, RBAC, reverse proxy, PII/secret redaction (privacy-filter.cpp, Presidio), audit logging, cosign signing, GGUF checksums, Llama Guard
   - *Performance*: quantization (GGUF/AWQ/GPTQ/FP8), speculative decoding, continuous batching, prefix caching, parallelism; benchmarking (llama-bench, p50/p95/p99)
   - *Correctness*: structured output (GBNF, xgrammar, guidance), RAG grounding (Chroma/FAISS), evals (HumanEval/MBPP, perplexity)
6. **C++-tuned models** — Qwen2.5-Coder, DeepSeek-Coder-V2, Codestral, StarCoder2, CodeLlama
7. **IDE integration** — Continue.dev, Tabby extensions, llama.vscode, Cline/Roo
8. **Recommended reference architecture** + **Risks & mitigations** + **References**

## Recommendation (preview)

Primary: **vLLM** for centralized NVIDIA GPU serving; **llama.cpp/llama-server** for CPU-only nodes; optionally front with **LocalAI** for native multi-user auth/quotas/PII redaction. Developer experience via **Tabby** (FIM + repo RAG) and/or **Continue.dev**. C++ models: **Qwen2.5-Coder** / **DeepSeek-Coder-V2**.

## Target file

- `local_llm_options.md` (workspace root)

## Further Considerations

1. Should the document include a concrete deployment example (Docker Compose / Kubernetes manifest for vLLM + gateway), or stay vendor-neutral prose? *Recommend: include one Compose snippet.*
2. Include a quantitative VRAM/throughput sizing table (model size vs GPU memory vs tokens/s)? *Recommend: yes, as an appendix.*
