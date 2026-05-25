# Core pattern called by an agent
# 1. Prepare Context  →  Combine task + instructions + memory + history
# 2. Call Model       →  Send context to LLM, get response
# 3. Handle Response  →  If text, we're done. If tool calls, execute them.
# 4. Iterate          →  Add tool results to context, go back to step 2
# 5. Return           →  Final response ready

import json
import logging
import re

from langchain_ollama import OllamaLLM


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define maximum history length for bounded memory
MAX_HISTORY_LENGTH = 100

#llm = OllamaLLM(model="mistral")
llm = OllamaLLM(model="llama3.2:1b")

def add_numbers(a: float, b: float):
    return a + b

tools = {
    "add_numbers": add_numbers
}

TOOLS_SCHEMA = """
Available tools:
- add_numbers: adds two numbers. action_input: {"a": <number>, "b": <number>}

When the answer is known, use action "finish" with action_input: {"answer": <value>}
"""

SYSTEM_PROMPT = """
You are an autonomous agent. Respond with ONE JSON object and nothing else — no prose, no markdown, no code fences.

Output format:
{"thought": "...", "action": "<tool_name or finish>", "action_input": {<key-value pairs>}}

Rules:
- Use ONLY the tools listed below.
- Do NOT invent tool names.
- Do NOT add any text outside the JSON object.
"""

def add_to_history(history, entry):
    """Add an entry to history, ensuring it stays within the maximum length."""
    history.append(entry)
    if len(history) > MAX_HISTORY_LENGTH:
        history.pop(0)

def execute_tool(action, action_input):
    """Validate and execute the specified tool."""
    if action not in tools:
        raise ValueError(f"Unknown tool: {action}")
    tool_fn = tools[action]
    return tool_fn(**action_input)

def agent_loop(goal):
    history = []

    while True:
        prompt = SYSTEM_PROMPT + TOOLS_SCHEMA + "\n" + \
                 f"Goal: {goal}\n" + \
                 f"History: {json.dumps(history)}\n"

        try:
            response = llm.invoke(prompt)
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if not match:
                raise json.JSONDecodeError("No JSON object found", response, 0)
            step = json.loads(match.group())
            thought = step["thought"]
            action = step["action"]
            action_input = step["action_input"]
        except (json.JSONDecodeError, KeyError) as e:
            logger.error("Error parsing response: %s\nRaw response: %s", e, response)
            yield {"type": "error", "message": f"Parse error: {e}"}
            continue

        logger.info("Thought: %s", thought)

        if action == "finish":
            answer = action_input.get("answer", "No answer provided")
            logger.info("Final Answer: %s", answer)
            yield {"type": "finish", "thought": thought, "answer": answer}
            break

        try:
            result = execute_tool(action, action_input)
        except Exception as e:
            logger.error("Error executing tool '%s': %s", action, e)
            yield {"type": "error", "message": f"Tool error ({action}): {e}"}
            continue

        yield {"type": "step", "thought": thought, "action": action, "action_input": action_input, "result": result}

        # Add observation to history
        add_to_history(history, {
            "thought": thought,
            "action": action,
            "input": action_input,
            "result": result
        })