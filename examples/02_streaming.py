"""
Example 02 — Streaming Responses
---------------------------------
Streams tokens to stdout as they are generated, giving a real-time typing
effect rather than waiting for the full response.

Prerequisites:
    ollama serve
    ollama pull llama3.2:3b

Run:
    python examples/02_streaming.py
"""

import ollama
from rich.console import Console
from rich.live import Live
from rich.text import Text


MODEL = "llama3.2:3b"
console = Console()


def stream_to_stdout(prompt: str, model: str = MODEL) -> str:
    """Stream response tokens to stdout; return full text when done."""
    full_response = ""
    with Live(Text(""), refresh_per_second=20, console=console) as live:
        for chunk in ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        ):
            token = chunk.message.content
            full_response += token
            live.update(Text(full_response))

    return full_response


def stream_openai_compat(prompt: str, model: str = MODEL) -> None:
    """Same streaming but via Ollama's OpenAI-compatible /v1 endpoint."""
    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required by the client but unused by Ollama
    )

    console.print(f"\n[bold cyan]OpenAI-compat stream ({model}):[/bold cyan]")
    full = ""
    for chunk in client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        token = chunk.choices[0].delta.content or ""
        full += token
        print(token, end="", flush=True)
    print()


if __name__ == "__main__":
    prompt = (
        "Explain the difference between CPU and GPU inference for LLMs "
        "in three concise bullet points."
    )

    console.print(f"\n[bold green]Ollama native stream ({MODEL}):[/bold green]")
    stream_to_stdout(prompt)

    stream_openai_compat(prompt)
