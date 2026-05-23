from langgraph.graph import StateGraph, END, START
from src.langgraphagenticai.state.state import state

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(state)

    def basic_chatbot_build_graph(self):

        self.graph_builder.add_node("chatBot","")
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)