import json
import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage

class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message,config):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.config = config or {"configurable": {"thread_id": "default-thread"}}

    def display_result(self):
        if self.usecase == "Basic Chatbot":
            # Display conversation history
            try:
                state_snapshot = self.graph.get_state(self.config)
                history = state_snapshot.values.get("messages", [])
                for msg in history:
                    role = "user" if msg.type == "human" else "assistant"
                    with st.chat_message(role):
                        st.write(msg.content)
            except Exception as e:
                print(f"Error fetching history: {e}")

            # Display the current user message
            with st.chat_message("user"):
                st.write(self.user_message)

            # Stream response using the checkpointer config
            for event in self.graph.stream(
                {"messages": [{"role": "user", "content": self.user_message}]},
                config=self.config
            ):
                print(event.values())
                for value in event.values():
                    messages = value.get('messages')
                    if messages:
                        with st.chat_message("assistant"):
                            if isinstance(messages, list):
                                st.write(messages[-1].content)
                            elif hasattr(messages, 'content'):
                                st.write(messages.content)
                            else:
                                st.write(str(messages))

        elif self.usecase == "Chatbot with Tools":
            # Display conversation history
            try:
                state_snapshot = self.graph.get_state(self.config)
                history = state_snapshot.values.get("messages", [])
                for msg in history:
                    if isinstance(msg, HumanMessage) or getattr(msg, "type", None) == "human":
                        with st.chat_message("user"):
                            st.write(msg.content)
                    elif isinstance(msg, AIMessage) or getattr(msg, "type", None) == "ai":
                        if msg.content:
                            with st.chat_message("assistant"):
                                st.write(msg.content)
                    elif isinstance(msg, ToolMessage) or getattr(msg, "type", None) == "tool":
                        with st.chat_message("tool"):
                            st.write("Tool Call start")
                            st.write(msg.content)
                            st.write("Tool Call end")
            except Exception as e:
                print(f"Error fetching history: {e}")

            # Display the current user message
            with st.chat_message("user"):
                st.write(self.user_message)

            # Stream response using the checkpointer config
            for event in self.graph.stream(
                {"messages": [{"role": "user", "content": self.user_message}]},
                config=self.config
            ):
                for node_name, value in event.items():
                    messages = value.get("messages")
                    if messages:
                        if not isinstance(messages, list):
                            messages = [messages]
                        for msg in messages:
                            if (isinstance(msg, AIMessage) or getattr(msg, "type", None) == "ai") and msg.content:
                                with st.chat_message("assistant"):
                                    st.write(msg.content)
                            elif isinstance(msg, ToolMessage) or getattr(msg, "type", None) == "tool":
                                with st.chat_message("tool"):
                                    st.write("Tool Call start")
                                    st.write(msg.content)
                                    st.write("Tool Call end")

        elif self.usecase == "AI News":
            with st.chat_message("user"):
                st.write(self.user_message)
            
            with st.spinner("Fetching and summarizing latest AI News..."):
                res = self.graph.invoke(
                    {"messages": [{"role": "user", "content": self.user_message}]},
                    config=self.config
                )
            
            summary = res.get("summary")
            filename = res.get("filename")
            if summary:
                with st.chat_message("assistant"):
                    st.write(summary)
                    if filename:
                        st.info(f"Summary saved to `{filename}`")