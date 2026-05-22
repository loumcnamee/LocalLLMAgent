"""
Example 05 — OpenAI-Compatible API Usage
-----------------------------------------
Ollama exposes an OpenAI-compatible REST API at http://localhost:11434/v1.
This means any code written for the OpenAI SDK can be pointed at Ollama
with a single base_url change — no API key needed.

This example shows:
  - Drop-in replacement for openai.ChatCompletion
  - Listing available local models via the models endpoint
  - Structured JSON output using response_format
  - Function/tool calling

Prerequisites:
    ollama serve
    ollama pull llama3.2:3b

Run:
    python examples/05_openai_compat_api.py
"""

import json
from openai import OpenAI


OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL = "llama3.2:3b"

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


# ── 1. List available models ──────────────────────────────────────────────────
def list_models() -> list[str]:
    models = client.models.list()
    return [m.id for m in models.data]


# ── 2. Basic chat completion ──────────────────────────────────────────────────
def chat(prompt: str, system: str = "You are a helpful assistant.") -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


# ── 3. Structured JSON output ─────────────────────────────────────────────────
def extract_structured(text: str) -> dict:
    """
    Ask the model to extract structured data from free text and return JSON.
    Note: not all local models support response_format=json_object reliably;
    prompting for JSON in the system message is the most portable approach.
    """
    system = (
        "You extract information from text and return ONLY valid JSON with no "
        "additional commentary. Use this schema: "
        '{"name": str, "date": str, "location": str, "summary": str}'
    )
    raw = chat(text, system=system)
    # Strip markdown code fences if the model wraps the JSON
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


# ── 4. Simple tool / function calling ────────────────────────────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. 'Brisbane'"},
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit",
                    },
                },
                "required": ["city"],
            },
        },
    }
]


def fake_weather_api(city: str, unit: str = "celsius") -> dict:
    """Simulated weather API response."""
    return {"city": city, "temperature": 22, "unit": unit, "condition": "Partly cloudy"}


def tool_call_demo(user_query: str) -> str:
    """Demonstrate function/tool calling via the OpenAI-compat API."""
    messages = [{"role": "user", "content": user_query}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    choice = response.choices[0]
    if choice.finish_reason == "tool_calls":
        tool_call = choice.message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        weather_data = fake_weather_api(**args)

        # Feed the tool result back to the model
        messages.append(choice.message)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(weather_data),
            }
        )
        final = client.chat.completions.create(model=MODEL, messages=messages)
        return final.choices[0].message.content
    else:
        return choice.message.content


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Available local models:", list_models())
    print()

    print("=== Basic chat ===")
    print(chat("What are the three laws of robotics?"))
    print()

    print("=== Structured extraction ===")
    sample_text = (
        "The annual PyConAU conference will be held on 23 August 2025 in Adelaide. "
        "It brings together Python developers from across Australia and New Zealand."
    )
    try:
        data = extract_structured(sample_text)
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError as exc:
        print(f"JSON parse failed (model may not have returned clean JSON): {exc}")
    print()

    print("=== Tool calling ===")
    result = tool_call_demo("What's the weather like in Brisbane right now?")
    print(result)
