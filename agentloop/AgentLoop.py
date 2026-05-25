

# Core pattern called by an agent
# 1. Prepare Context  →  Combine task + instructions + memory + history
# 2. Call Model       →  Send context to LLM, get response
# 3. Handle Response  →  If text, we're done. If tool calls, execute them.
# 4. Iterate          →  Add tool results to context, go back to step 2
# 5. Return           →  Final response ready

import json

from langchain_community.llms import Ollama

llm = Ollama(model="mistral")

def add_numbers(a: float, b: float):
    return a + b

tools = {
    "add_numbers": add_numbers
}

SYSTEM_PROMPT = """
You are an autonomous agent. 
Use this loop:
1. Think about the problem.
2. Decide which tool to use.
3. Output ONLY in this JSON format:

{
  "thought": "...",
  "action": "tool_name or 'finish'",
  "action_input": { ... }
}
"""

def agent_loop(goal):
    history = []

    while True:
        prompt = SYSTEM_PROMPT + "\n\n" + \
                 f"Goal: {goal}\n" + \
                 f"History: {history}\n"

        response = llm(prompt)
        step = json.loads(response)

        thought = step["thought"]
        action = step["action"]
        action_input = step["action_input"]

        print("Thought:", thought)

        if action == "finish":
            print("Final Answer:", action_input["answer"])
            break

        # Execute tool
        tool_fn = tools[action]
        result = tool_fn(**action_input)

        # Add observation to history
        history.append({
            "thought": thought,
            "action": action,
            "input": action_input,
            "result": result
        })