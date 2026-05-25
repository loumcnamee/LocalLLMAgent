import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from AgentLoop import agent_loop

def main():
    st.title("Agent Loop UI")

    goal = st.text_input("Enter the goal for the agent:")

    if st.button("Run Agent Loop"):
        if not goal:
            st.warning("Please enter a goal before running the agent loop.")
            return

        st.write("### Agent Output")
        try:
            for event in agent_loop(goal):
                if event["type"] == "step":
                    with st.expander(f"Tool: `{event['action']}`", expanded=True):
                        st.write(f"**Thought:** {event['thought']}")
                        st.write(f"**Input:** `{event['action_input']}`")
                        st.write(f"**Result:** `{event['result']}`")
                elif event["type"] == "finish":
                    st.success(f"**Final Answer:** {event['answer']}")
                    st.write(f"*Thought: {event['thought']}*")
                elif event["type"] == "error":
                    st.error(event["message"])
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()