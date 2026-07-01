# Notes from Manual Research

## Q: List options to host LLMs locally. For each option identify OS, model types supported, dependencies. Also for each option rate performance, scalability, IDE integration, license and security.

The four best options to host LLMs locally for software development are detailed below. Each tool acts as a local server that connects to your IDE. [1] 

## 1. Ollama
The most popular tool for running local LLMs due to its simplicity, speed, and active ecosystem. [2, 3, 4, 5] 

* OS: macOS, Linux, Windows.
* Model Types Supported: GGUF.
* Dependencies: No external dependencies. Self-contained executable.
* Performance: Excellent. Uses llama.cpp backend with automated GPU acceleration (NVIDIA, AMD, Apple Silicon).
* Scalability: Moderate. Handles multiple model loads but lacks advanced enterprise cluster orchestration.
* IDE Integration: Excellent. Native support in Continue, Twinny, and Llama Coder.
* License: MIT License (Open Source).
* Security: High. Runs completely offline by default. No telemetry unless opted in. [6, 7, 8, 9, 10] 

## 2. LM Studio
A user-friendly desktop application featuring a clean graphical interface and a built-in Hugging Face model explorer. [11, 12, 13, 14] 

* OS: macOS, Windows, Linux.
* Model Types Supported: GGUF, MLX (on Apple Silicon).
* Dependencies: Requires a desktop GUI environment.
* Performance: Excellent. Highly optimized hardware configuration toggles for CPU/GPU offloading.
* Scalability: Low. Designed primarily as a single-user desktop application.
* IDE Integration: Excellent. Exposes an OpenAI-compatible API endpoint (/v1/chat/completions) for any IDE extension.
* License: Free for personal use. Requires a paid subscription for commercial/enterprise use.
* Security: High. Local-first architecture. It does not network your prompt data to external servers. [15, 16, 17, 18, 19] 

## 3. vLLM
A high-throughput, industrial-grade LLM serving engine built for speed and heavy concurrent workloads. [20, 21, 22, 23] 

* OS: Linux (Windows supported via WSL).
* Model Types Supported: AWQ, GPTQ, SqueezeLLM, unquantized FP16/BF16.
* Dependencies: Python, PyTorch, CUDA (NVIDIA GPU required for optimal performance).
* Performance: Industry-Best. Uses PagedAttention to maximize throughput and minimize VRAM waste.
* Scalability: Very High. Built for multi-GPU setups, distributed serving, and high-concurrency enterprise workloads.
* IDE Integration: Good. Provides an OpenAI-compatible API server that works easily with VS Code extensions.
* License: Apache 2.0 License (Open Source).
* Security: High. Fully self-hosted, though security depends on how you secure your local network ports. [24, 25, 26, 27, 28] 

## 4. Llama.cpp
The foundational, raw C/C++ engine that powers most local LLM tools (including Ollama and LM Studio). [29, 30, 31, 32, 33] 

* OS: macOS, Linux, Windows, FreeBSD.
* Model Types Supported: GGUF.
* Dependencies: C/C++ compiler (make, cmake).
* Performance: Great. Highly optimized for CPU inference and tailored for Apple Silicon (Metal).
* Scalability: Moderate. Supports basic concurrent requests but requires manual configuration.
* IDE Integration: Moderate. Requires launching the built-in server binary to expose an API endpoint.
* License: MIT License (Open Source).
* Security: High. Minimalist, transparent codebase with no tracking or external data leakage. [34, 35, 36, 37, 38] 

------------------------------
To help find the right backend for your workflow, please consider the following next steps.

* Do you plan to host this on a single developer machine or deploy it on a shared local team server?
* Are you looking for a tool with a graphical user interface or a headless command-line/API tool?
* Do you have an NVIDIA GPU, Apple Silicon (M-series) chip, or a CPU-only system? [39, 40, 41] 


[1] [https://blog.dailydoseofds.com](https://blog.dailydoseofds.com/p/4-ways-to-run-llms-locally)
[2] [https://www.cognativ.com](https://www.cognativ.com/blogs/post/local-llm-for-python-coding-top-picks-and-insights/261)
[3] [https://community.sap.com](https://community.sap.com/t5/artificial-intelligence-blogs-posts/bring-open-source-llms-into-sap-ai-core/ba-p/13655167)
[4] [https://medium.com](https://medium.com/@jaegercode/openai-returns-to-open-source-complete-guide-to-gpt-oss-local-deployment-d912a28298db)
[5] [https://jomasego.medium.com](https://jomasego.medium.com/using-the-new-chatgpt-agent-or-building-your-own-dbaf7122e388)
[6] [https://www.pugetsystems.com](https://www.pugetsystems.com/labs/articles/tech-primer-what-hardware-do-you-need-to-run-a-local-llm/)
[7] [https://www.linkedin.com](https://www.linkedin.com/pulse/build-your-local-ai-coding-agent-cloud-needed-louis-fran%C3%A7ois-bouchard-yluce)
[8] [https://support.plmgroup.eu](https://support.plmgroup.eu/hc/da/articles/4805393228957-SOLIDWORKS-and-Mac)
[9] [https://ai.plainenglish.io](https://ai.plainenglish.io/andrej-karpathy-software-1-0-software-2-0-and-software-3-0-where-ai-is-heading-7ebc4ac582be)
[10] [https://www.openxcell.com](https://www.openxcell.com/blog/llama-cpp-vs-ollama/)
[11] [https://www.sitepoint.com](https://www.sitepoint.com/local-llms-complete-guide/)
[12] [https://www.binadox.com](https://www.binadox.com/blog/best-local-llms-for-cost-effective-ai-development-in-2025/)
[13] [https://todatabeyond.substack.com](https://todatabeyond.substack.com/p/5-tools-to-run-large-language-models)
[14] [https://www.codiste.com](https://www.codiste.com/lm-studio-vs-ollama)
[15] [https://medium.com](https://medium.com/@bonnyjames0830/a-comprehensive-guide-to-using-local-llms-offline-3bf63f6a400d)
[16] [https://verpex.com](https://verpex.com/blog/operating-systems-common-in-cloud-data-centers)
[17] [https://mokkappsdev.medium.com](https://mokkappsdev.medium.com/boost-your-productivity-by-using-the-terminal-iterm-zsh-1af800d2d0c6)
[18] [https://support.plmgroup.eu](https://support.plmgroup.eu/hc/da/articles/4805393228957-SOLIDWORKS-and-Mac)
[19] [https://arpitkulsh.medium.com](https://arpitkulsh.medium.com/lm-studio-the-desktop-ai-lab-that-brings-powerful-llms-to-your-own-machine-687b40ca69e4)
[20] [https://www.linkedin.com](https://www.linkedin.com/pulse/qwen3-self-hosting-guide-vllm-sglang-maksym-huczynski-i4v2f)
[21] [https://medium.com](https://medium.com/@eliran89c/how-to-deploy-a-self-hosted-llm-on-eks-and-why-you-should-e9184e366e0a)
[22] [https://medium.com](https://medium.com/@palash-fin/mastering-vllm-on-aks-deployment-monitoring-troubleshooting-guide-36893e01f2b6)
[23] [https://medium.com](https://medium.com/@nimritakoul01/llm-inference-providers-7b374695a0a0)
[24] [https://www.pugetsystems.com](https://www.pugetsystems.com/labs/articles/tech-primer-what-hardware-do-you-need-to-run-a-local-llm/)
[25] [https://docs.agentops.ai](https://docs.agentops.ai/v2/self-hosting/overview)
[26] [https://codingnomads.com](https://codingnomads.com/hardware-and-operating-system-setup-for-python-101)
[27] [https://www.spheron.network](https://www.spheron.network/blog/modular-max-mojo-gpu-cloud-llm-inference/)
[28] [https://www.sitepoint.com](https://www.sitepoint.com/ollama-vs-vllm-scaling-local-ai-stack/)
[29] [https://pinggy.io](https://pinggy.io/blog/top_5_local_llm_tools_and_models/)
[30] [https://www.datacamp.com](https://www.datacamp.com/tutorial/run-llms-locally-tutorial)
[31] [https://todatabeyond.substack.com](https://todatabeyond.substack.com/p/5-tools-to-run-large-language-models)
[32] [https://semaphore.io](https://semaphore.io/blog/local-llm)
[33] [https://apxml.com](https://apxml.com/courses/getting-started-local-llms/chapter-4-running-first-local-llm/intro-local-llm-runners)
[34] [https://www.pugetsystems.com](https://www.pugetsystems.com/labs/articles/tech-primer-what-hardware-do-you-need-to-run-a-local-llm/)
[35] [https://medium.com](https://medium.com/data-science-collective/how-to-run-an-open-source-llm-on-your-personal-computer-bc6cca454282)
[36] [https://www.deepin.org](https://www.deepin.org/en/llamafile-a-must-have-tool/)
[37] [https://github.com](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/local-llm-on-mac.md)
[38] [https://levelup.gitconnected.com](https://levelup.gitconnected.com/i-tried-20-open-source-llms-these-5-perform-remarkably-well-on-cpus-769a57bb98bd)
[39] [https://docs.tabulareditor.com](https://docs.tabulareditor.com/en/features/ai-assistant.html)
[40] [https://llm.mlc.ai](https://llm.mlc.ai/docs/get_started/introduction)
[41] [https://www.xda-developers.com](https://www.xda-developers.com/rtx-5090-cant-keep-up-apple-silicon-biggest-local-llms/)


## What are the options to integrate the VS Code and Visual Studio IDEs with locally hosted LLMs?

You can connect both Visual Studio Code and Visual Studio to local LLMs like Ollama or LM Studio. Most extensions achieve this by pointing their API base URL to your local server (e.g., http://localhost:11434 for Ollama). [1, 2, 3, 4, 5] 
Here are the best options to integrate local LLMs into your development workflow.
## Visual Studio Code Extensions

* [Continue.dev](https://www.continue.dev/): The most popular open-source AI assistant for VS Code. It provides a chat sidebar, inline code generation (Cmd/Ctrl + I), and codebase indexing. It natively supports Ollama, LM Studio, and Llama.cpp. [6, 7, 8, 9, 10] 
* Twinny: A highly efficient, privacy-focused extension built specifically for local LLMs. It offers tab-completion (fill-in-the-middle) and a chat interface without telemetry. [11, 12] 
* [Codeium](https://codeium.com/): While primarily cloud-based, Codeium offers an enterprise self-hosted option that can run on local servers or private clouds for teams requiring strict data isolation. [13, 14, 15, 16, 17] 
* Ollama Autocomplete: A lightweight extension dedicated strictly to fast, local, single-line code completions as you type.

## Visual Studio (Enterprise/Community) Options

* Built-in GitHub Copilot: Visual Studio 2022 and newer include deep, native Copilot integration. However, it requires a paid cloud subscription and cannot easily point to a completely offline, local LLM backend. [18, 19, 20, 21] 
* [Refact.ai](https://refact.ai/): An AI coding assistant that supports Visual Studio. It allows you to self-host its enterprise backend locally and connect the Visual Studio plugin directly to your own server. [22, 23] 
* Custom API Proxying: Visual Studio lacks the vast open-source extension ecosystem of VS Code for local LLMs. Developers often use Continue.dev or Twinny in VS Code, or route Visual Studio traffic through a local proxy that mimics the OpenAI API schema. [24, 25, 26, 27] 

## Recommended Model Pairings
For a smooth local coding experience, use models trained specifically for development:

* Qwen2.5-Coder (7B or 14B): The current gold standard for local code generation and reasoning.
* DeepSeek-Coder (6.7B): Highly efficient for autocomplete tasks and lightweight hardware.
* Codellama: Meta's developer-focused model, excellent for broad language support. [28, 29, 30, 31, 32] 

To get started, launch your local backend (like Ollama), install Continue in VS Code, and update your config.json file to point to your local model. [33, 34] 
To help you get this running smoothly, please share a bit more about your development setup and goals.

* Do you prefer inline tab-completions as you type, or a sidebar chat to ask architecture questions?
* Which programming languages do you work with most frequently?
* What are your computer's hardware specs (specifically RAM and GPU)?


[1] [https://techcommunity.microsoft.com](https://techcommunity.microsoft.com/blog/educatordeveloperblog/visual-studio-code-ai-toolkit-run-llms-locally/4163192)
[2] [https://docs.pieces.app](https://docs.pieces.app/products/extensions-plugins/visual-studio/copilot/llm-settings)
[3] [https://ai.gopubby.com](https://ai.gopubby.com/serving-llms-using-lm-studio-1d31bb776a60)
[4] [https://mehmetozkaya.medium.com](https://mehmetozkaya.medium.com/semantic-search-development-with-c-using-ollama-vectordb-orchestrate-in-net-aspire-d82eec73696a)
[5] [https://blog.gopenai.com](https://blog.gopenai.com/building-a-local-llm-powered-c-agent-for-code-analysis-and-developer-assistance-596692583d7d)
[6] [https://github.com](https://github.com/redhat-developer/vscode-paver)
[7] [https://www.reddit.com](https://www.reddit.com/r/neovim/comments/1haxgd5/currently_most_active_ollama_based_completion/)
[8] [https://thenewstack.io](https://thenewstack.io/how-to-integrate-vs-code-with-ollama-for-local-ai-assistance/)
[9] [https://www.infoworld.com](https://www.infoworld.com/article/4144487/i-ran-qwen3-5-locally-instead-of-claude-code-heres-what-happened.html)
[10] [https://huggingface.co](https://huggingface.co/learn/mcp-course/unit2/continue-client)
[11] [https://dev.to](https://dev.to/liukonen/unleashing-the-power-of-developer-ai-a-journey-into-hosting-a-private-llmcode-assistant-locally-4kma)
[12] [https://discuss.linuxcontainers.org](https://discuss.linuxcontainers.org/t/llama-cpp-and-ollama-servers-plugins-for-vs-code-vs-codium-and-intellij-ai/19744)
[13] [https://nimbalyst.com](https://nimbalyst.com/blog/best-local-first-ai-coding-tools-2026/)
[14] [https://www.vmware.com](https://www.vmware.com/docs/codeium-vcf-solution-brief)
[15] [https://www.devart.com](https://www.devart.com/dbforge/best-ai-coding-assistant-tools.html)
[16] [https://www.scrumlaunch.com](https://www.scrumlaunch.com/blog/best-ai-powered-ides-and-coding-assistants-2025)
[17] [https://www.sitepoint.com](https://www.sitepoint.com/local-ai-coding-assistant-vscode-ollama-continue/)
[18] [https://multishoring.com](https://multishoring.com/blog/microsoft-build-2025-session-schedule-whos-speaking-and-what-to-attend/)
[19] [https://ithy.com](https://ithy.com/article/best-llms-for-coding-y58dkg3f)
[20] [https://pureai.com](https://pureai.com/articles/2025/09/02/pros-and-cons-of-running-a-large-language-model-locally.aspx)
[21] [https://forum.dcs.world](https://forum.dcs.world/topic/379791-hybrid-voice-interaction-local-stttts-with-llm-integration/)
[22] [https://dev.to](https://dev.to/nilebits/15-most-powerful-ai-tools-every-developer-should-be-using-in-2025-2075)
[23] [https://medium.com](https://medium.com/@justinmilner/the-top-coding-assistant-platforms-of-july-2024-a862e84c1b34)
[24] [https://www.jrebel.com](https://www.jrebel.com/blog/vs-code-extension-for-jrebel)
[25] [https://discuss.linuxcontainers.org](https://discuss.linuxcontainers.org/t/llama-cpp-and-ollama-servers-plugins-for-vs-code-vs-codium-and-intellij-ai/19744)
[26] [https://medium.com](https://medium.com/@roanmonteiro/the-complete-beginners-guide-to-local-ai-concepts-models-hardware-and-a-working-pipeline-for-4a4b3de7b004)
[27] [https://chriskirby.net](https://chriskirby.net/run-a-free-ai-coding-assistant-locally-with-vs-code/)
[28] [https://www.sitepoint.com](https://www.sitepoint.com/run-local-llms-2026-complete-developer-guide/)
[29] [https://medium.com](https://medium.com/@muthu.venkataraman/getting-started-with-foundry-local-on-windows-a-surprisingly-powerful-local-ai-experience-339f5f079532)
[30] [https://failingfast.io](https://failingfast.io/local-coding-ai-models/)
[31] [https://www.xda-developers.com](https://www.xda-developers.com/local-ai-replaces-chatgpt-for-coding/)
[32] [https://keploy.io](https://keploy.io/blog/community/best-opensource-coding-ai)
[33] [https://juliangoldie.com](https://juliangoldie.com/ollama-claude-code-integration/)
[34] [https://www.linkedin.com](https://www.linkedin.com/pulse/self-hosting-ai-coding-assistant-using-continuedev-purihin-enriquez-8vy9c)
