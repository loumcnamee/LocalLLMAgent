"""
Example 01 — Basic Chat Completion via Ollama Python Client
-----------------------------------------------------------
Demonstrates synchronous and asynchronous chat with a local model.

Prerequisites:
    ollama serve  (running in background or as systemd service)
    ollama pull llama3.2:3b

Run:
    python examples/01_basic_chat.py
"""

import ollama


# MODEL = "llama3.2:3b"
MODEL = "llama3.2:1b" # Smaller model for faster responses in demo


def simple_chat(prompt: str) -> str:
    """Single-turn chat: send a prompt and return the response text."""
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content


def multi_turn_chat() -> None:
    """Multi-turn conversation that maintains history."""
    print(f"Chat with {MODEL}  (type 'quit' to exit)\n")
    history: list[dict] = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit", "q"}:
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        response = ollama.chat(model=MODEL, messages=history)
        assistant_msg = response.message.content

        history.append({"role": "assistant", "content": assistant_msg})
        print(f"\nAssistant: {assistant_msg}\n")


if __name__ == "__main__":
    # Quick single-turn demo
    answer = simple_chat("In one sentence, what is a large language model?")
    print(f"Single-turn response:\n{answer}\n")
    print("-" * 60)

    # Interactive multi-turn session
    multi_turn_chat()
