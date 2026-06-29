import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from AgentLoop import agent_loop

def main():
    st.title("Agent Loop UI")

    # Initialize session state for termination
    if "terminate_requested" not in st.session_state:
        st.session_state.terminate_requested = False
    if "agent_running" not in st.session_state:
        st.session_state.agent_running = False

    def should_terminate():
        return st.session_state.terminate_requested

    # Sidebar with terminate button
    with st.sidebar:
        if st.button("Shutdown Application"):
            st.session_state.terminate_requested = True
            st.warning("Shutting down...")
            os._exit(0)

    goal = st.text_input("Enter the goal for the agent:")

    if st.button("Run Agent Loop"):
        if not goal:
            st.warning("Please enter a goal before running the agent loop.")
            return

        # Reset termination flag and set running state
        st.session_state.terminate_requested = False
        st.session_state.agent_running = True

        st.write("### Agent Output")
        try:
            for event in agent_loop(goal, should_terminate=should_terminate):
                if event["type"] == "step":
                    with st.expander(f"Tool: `{event['action']}`", expanded=True):
                        st.write(f"**Thought:** {event['thought']}")
                        st.write(f"**Input:** `{event['action_input']}`")
                        st.write(f"**Result:** `{event['result']}`")
                elif event["type"] == "finish":
                    st.success(f"**Final Answer:** {event['answer']}")
                    st.write(f"*Thought: {event['thought']}*")
                elif event["type"] == "terminated":
                    st.warning(event["message"])
                elif event["type"] == "error":
                    st.error(event["message"])
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
        finally:
            st.session_state.agent_running = False
            st.session_state.terminate_requested = False

if __name__ == "__main__":
    main()