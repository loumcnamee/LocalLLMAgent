# Notes from Manual Research

## Q: What are the options to host local LLMs?



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
