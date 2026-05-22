"""
Example 04 — Code Generation
-----------------------------
Uses a locally-hosted model (e.g. gemma4:27b or llama3.1:8b) to generate,
explain, and review Python code.

Prerequisites:
    ollama serve
    ollama pull llama3.2:3b        # or whichever model you prefer
    ollama pull gemma4:27b         # optional, better at coding

Run:
    python examples/04_code_generation.py
"""

import ollama
from rich.console import Console
from rich.syntax import Syntax


console = Console()
MODEL = "llama3.2:3b"  # swap for gemma4:27b for higher quality


SYSTEM_PROMPT = (
    "You are an expert Python developer. "
    "Respond with clean, idiomatic Python code and brief explanations. "
    "Always include type hints and a short docstring."
)


def generate_code(task: str, model: str = MODEL) -> str:
    """Ask the model to write Python code for a given task description."""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Write Python code to: {task}"},
        ],
    )
    return response.message.content


def explain_code(code: str, model: str = MODEL) -> str:
    """Ask the model to explain what a piece of code does."""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Explain what this Python code does, line by line:\n\n```python\n{code}\n```",
            },
        ],
    )
    return response.message.content


def review_code(code: str, model: str = MODEL) -> str:
    """Ask the model to review code for bugs, style issues, and improvements."""
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Review this Python code. Identify bugs, style issues, and suggest "
                    f"concrete improvements:\n\n```python\n{code}\n```"
                ),
            },
        ],
    )
    return response.message.content


if __name__ == "__main__":
    # ── Task 1: generate ──────────────────────────────────────────────────────
    task = (
        "parse a CSV file with columns (timestamp, temperature_c, humidity_pct), "
        "compute hourly averages, and return the results as a list of dataclasses"
    )
    console.print(f"\n[bold green]TASK:[/bold green] {task}\n")
    generated = generate_code(task)
    console.print("[bold cyan]Generated code:[/bold cyan]")
    console.print(Syntax(generated, "python", theme="monokai", line_numbers=True))

    # ── Task 2: explain ───────────────────────────────────────────────────────
    snippet = """\
def fib(n: int, memo: dict[int, int] = {}) -> int:
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
"""
    console.print("\n[bold green]EXPLAIN:[/bold green]")
    console.print(Syntax(snippet, "python", theme="monokai"))
    explanation = explain_code(snippet)
    console.print(f"\n[bold cyan]Explanation:[/bold cyan]\n{explanation}")

    # ── Task 3: review ────────────────────────────────────────────────────────
    buggy = """\
def divide_all(numbers, divisor):
    results = []
    for n in numbers:
        results.append(n / divisor)
    return results
"""
    console.print("\n[bold green]REVIEW:[/bold green]")
    console.print(Syntax(buggy, "python", theme="monokai"))
    review = review_code(buggy)
    console.print(f"\n[bold cyan]Review:[/bold cyan]\n{review}")
