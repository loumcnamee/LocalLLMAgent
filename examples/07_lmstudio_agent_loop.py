"""
Example 07 — LMStudio Agent Loop (Unbiased Tool Usage)
------------------------------------------------------
An agent loop using the LMStudio OpenAI-compatible API that avoids
bias toward tool usage. The agent will:
  - Answer directly when no tools are needed
  - Use tools only when genuinely required
  - Maintain conversation history for multi-turn interactions

Key design principle: The agent should NOT force tool calls. It uses
`tool_choice="auto"` and prompting to let the model decide when tools
are actually necessary.

Prerequisites:
    LMStudio running with a model loaded (default port 1234)
    A model with function-calling support (e.g., Llama 3.x, Qwen 2.5)

Run:
    python examples/07_lmstudio_agent_loop.py
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Generator

from openai import OpenAI


# ── Configuration ─────────────────────────────────────────────────────────────
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
#MODEL = "lmstudio-community/qwen2.5-7b-instruct"  # Adjust to your loaded model
MODEL = "google/gemma-4-e2b"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── System Prompt (Unbiased Tool Usage) ───────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

IMPORTANT GUIDELINES:
1. Answer questions DIRECTLY when you already know the answer or can reason it out.
2. Only use tools when they are GENUINELY REQUIRED to complete the task.
3. Do NOT use tools just because they exist — use your own knowledge first.
4. For math, facts you know, reasoning tasks, or general knowledge: respond directly.
5. For tasks that REQUIRE external data or actions (weather, calculations you can't 
   do mentally, file operations, etc.): use the appropriate tool.

Examples of when to answer directly:
- "What is the capital of France?" → Answer directly (you know this)
- "Explain quantum entanglement" → Answer directly (knowledge question)
- "What is 2 + 2?" → Answer directly (trivial math)

Examples of when to use tools:
- "What's the weather in Tokyo right now?" → Use weather tool (real-time data)
- "Calculate 847293 * 938472" → Use calculator tool (complex computation)
- "Search for recent news about AI" → Use search tool (external data)

Be helpful, accurate, and efficient. Don't over-rely on tools."""


# ── Tool Definitions ──────────────────────────────────────────────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform arithmetic calculations. Use ONLY for complex math "
                           "that would be error-prone to compute mentally. Do NOT use for "
                           "simple operations like 2+2 or 10*5.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate, e.g., '(45.7 * 892) / 3.14'"
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a location. Use when the user asks "
                           "about current/real-time weather conditions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., 'Tokyo', 'New York'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit",
                        "default": "celsius"
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information. Use ONLY when you need "
                           "current/recent information you don't have, or when the user "
                           "explicitly asks to search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"],
            },
        },
    },
]


# ── Tool Implementations ──────────────────────────────────────────────────────
def calculator(expression: str) -> dict:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow safe math operations
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}
        result = eval(expression)  # Safe due to character filtering
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}


def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Simulated weather API (replace with real API in production)."""
    # Simulated data - in production, call a real weather API
    weather_data = {
        "Tokyo": {"temp": 18, "condition": "Partly cloudy", "humidity": 65},
        "New York": {"temp": 12, "condition": "Sunny", "humidity": 45},
        "London": {"temp": 8, "condition": "Rainy", "humidity": 80},
        "Sydney": {"temp": 24, "condition": "Clear", "humidity": 55},
    }
    
    city_data = weather_data.get(location, {"temp": 20, "condition": "Unknown", "humidity": 50})
    temp = city_data["temp"]
    if unit == "fahrenheit":
        temp = (temp * 9/5) + 32
    
    return {
        "location": location,
        "temperature": temp,
        "unit": unit,
        "condition": city_data["condition"],
        "humidity": city_data["humidity"],
    }


def search_web(query: str) -> dict:
    """Simulated web search (replace with real API in production)."""
    # Simulated search results
    return {
        "query": query,
        "results": [
            {"title": f"Result 1 for: {query}", "snippet": "This is a simulated search result."},
            {"title": f"Result 2 for: {query}", "snippet": "Another simulated result for demo purposes."},
        ],
        "note": "This is simulated data. Integrate a real search API for production use."
    }


# Tool registry
TOOL_REGISTRY: dict[str, Callable] = {
    "calculator": calculator,
    "get_current_weather": get_current_weather,
    "search_web": search_web,
}


# ── Agent Loop Implementation ─────────────────────────────────────────────────
@dataclass
class AgentConfig:
    """Configuration for the agent loop."""
    base_url: str = LMSTUDIO_BASE_URL
    model: str = MODEL
    max_iterations: int = 10
    temperature: float = 0.7
    max_history: int = 50


@dataclass
class AgentState:
    """Maintains agent state across iterations."""
    messages: list[dict] = field(default_factory=list)
    iteration: int = 0
    tool_calls_made: int = 0
    direct_responses: int = 0


@dataclass
class AgentResponse:
    """Response from an agent loop iteration."""
    type: str  # "message", "tool_call", "error", "max_iterations"
    content: str | None = None
    tool_name: str | None = None
    tool_args: dict | None = None
    tool_result: Any | None = None
    thought: str | None = None


def execute_tool(name: str, arguments: dict) -> Any:
    """Execute a tool by name with given arguments."""
    if name not in TOOL_REGISTRY:
        return {"error": f"Unknown tool: {name}"}
    
    try:
        return TOOL_REGISTRY[name](**arguments)
    except Exception as e:
        logger.error(f"Tool execution error ({name}): {e}")
        return {"error": str(e)}


def agent_loop(
    user_input: str,
    config: AgentConfig | None = None,
    state: AgentState | None = None,
    should_terminate: Callable[[], bool] | None = None,
) -> Generator[AgentResponse, None, AgentState]:
    """
    Run the agent loop with unbiased tool usage.
    
    Args:
        user_input: The user's message/query
        config: Agent configuration (uses defaults if None)
        state: Existing state for multi-turn conversations (creates new if None)
        should_terminate: Optional callback to check for early termination
    
    Yields:
        AgentResponse objects for each step (tool calls, messages, etc.)
    
    Returns:
        Final AgentState for continuation
    """
    config = config or AgentConfig()
    state = state or AgentState()
    
    # Initialize OpenAI client for LMStudio
    client = OpenAI(base_url=config.base_url, api_key="lm-studio")
    
    # Initialize conversation if empty
    if not state.messages:
        state.messages.append({"role": "system", "content": SYSTEM_PROMPT})
    
    # Add user message
    state.messages.append({"role": "user", "content": user_input})
    
    # Trim history if needed
    while len(state.messages) > config.max_history:
        # Keep system message, remove oldest user/assistant pairs
        if state.messages[1]["role"] != "system":
            state.messages.pop(1)
        else:
            state.messages.pop(2)
    
    while state.iteration < config.max_iterations:
        state.iteration += 1
        
        # Check for termination
        if should_terminate and should_terminate():
            yield AgentResponse(type="terminated", content="Agent loop terminated by user.")
            return state
        
        logger.info(f"Iteration {state.iteration}: Calling model...")
        
        try:
            # Call model with tool_choice="auto" - let the model decide
            response = client.chat.completions.create(
                model=config.model,
                messages=state.messages,
                tools=TOOLS,
                tool_choice="auto",  # Key: Let model decide, don't force tools
                temperature=config.temperature,
            )
        except Exception as e:
            logger.error(f"Model call failed: {e}")
            yield AgentResponse(type="error", content=f"Model error: {e}")
            return state
        
        choice = response.choices[0]
        message = choice.message
        
        # Check if model wants to use tools
        if choice.finish_reason == "tool_calls" and message.tool_calls:
            # Model decided to use tools
            state.messages.append(message.model_dump())
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}
                
                logger.info(f"Tool call: {tool_name}({tool_args})")
                
                # Execute the tool
                result = execute_tool(tool_name, tool_args)
                state.tool_calls_made += 1
                
                yield AgentResponse(
                    type="tool_call",
                    tool_name=tool_name,
                    tool_args=tool_args,
                    tool_result=result,
                )
                
                # Add tool result to messages
                state.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                })
            
            # Continue loop to get model's response after tool execution
            continue
        
        else:
            # Model chose to respond directly (no tool call)
            content = message.content or ""
            state.messages.append({"role": "assistant", "content": content})
            state.direct_responses += 1
            
            logger.info(f"Direct response (no tools used)")
            
            yield AgentResponse(type="message", content=content)
            return state
    
    # Max iterations reached
    yield AgentResponse(
        type="max_iterations",
        content=f"Reached maximum iterations ({config.max_iterations})"
    )
    return state


# ── Interactive Chat Interface ────────────────────────────────────────────────
def interactive_chat():
    """Run an interactive chat session with the agent."""
    print("=" * 60)
    print("LMStudio Agent Loop - Unbiased Tool Usage")
    print("=" * 60)
    print("Type 'quit' to exit, 'stats' to see usage statistics")
    print("The agent will answer directly when possible,")
    print("and only use tools when genuinely needed.")
    print("=" * 60)
    print()
    
    config = AgentConfig()
    state = AgentState()
    
    # Test connection
    try:
        client = OpenAI(base_url=config.base_url, api_key="lm-studio")
        models = client.models.list()
        available = [m.id for m in models.data]
        print(f"Connected to LMStudio. Available models: {available[:3]}...")
        if config.model not in available and available:
            config.model = available[0]
            print(f"Using model: {config.model}")
    except Exception as e:
        print(f"Warning: Could not connect to LMStudio at {config.base_url}")
        print(f"Error: {e}")
        print("Make sure LMStudio is running with a model loaded.")
        return
    
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break
        
        if user_input.lower() == "stats":
            print(f"\n--- Statistics ---")
            print(f"Iterations: {state.iteration}")
            print(f"Tool calls made: {state.tool_calls_made}")
            print(f"Direct responses: {state.direct_responses}")
            if state.tool_calls_made + state.direct_responses > 0:
                ratio = state.direct_responses / (state.tool_calls_made + state.direct_responses)
                print(f"Direct response ratio: {ratio:.1%}")
            print(f"Message history: {len(state.messages)} messages")
            print()
            continue
        
        print()
        
        # Run agent loop
        for response in agent_loop(user_input, config=config, state=state):
            if response.type == "tool_call":
                print(f"  [Tool: {response.tool_name}]")
                print(f"  Args: {response.tool_args}")
                print(f"  Result: {json.dumps(response.tool_result, indent=2)}")
                print()
            elif response.type == "message":
                print(f"Assistant: {response.content}")
            elif response.type == "error":
                print(f"Error: {response.content}")
            elif response.type == "max_iterations":
                print(f"Warning: {response.content}")
        
        print()


# ── Demo: Test Both Direct and Tool-Based Responses ──────────────────────────
def demo():
    """Demonstrate that the agent uses tools only when needed."""
    print("=" * 60)
    print("Demo: Unbiased Tool Usage")
    print("=" * 60)
    print()
    
    config = AgentConfig()
    
    # Test queries - mix of direct-answer and tool-requiring
    test_queries = [
        # Should answer directly (no tools needed)
        "What is the capital of Japan?",
        "Explain what a neural network is in simple terms.",
        "What is 7 + 5?",
        
        # Should use tools
        "What's the current weather in Tokyo?",
        "Calculate 8472.93 * 3847.21",
        "Search for recent developments in quantum computing",
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        print("-" * 40)
        
        state = AgentState()
        tool_used = False
        
        for response in agent_loop(query, config=config, state=state):
            if response.type == "tool_call":
                tool_used = True
                print(f"  → Used tool: {response.tool_name}")
            elif response.type == "message":
                # Truncate long responses
                content = response.content[:200] + "..." if len(response.content) > 200 else response.content
                print(f"  → Response: {content}")
        
        if not tool_used:
            print("  → Answered directly (no tools)")
        
        print()


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        interactive_chat()
