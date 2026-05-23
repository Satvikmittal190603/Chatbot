from langgraph.graph import StateGraph, END, START
from src.langgraphagenticai.state.state import state
from src.langgraphagenticai.nodes.basicChatbotNode import basicChatbotNode

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(state)

    def basic_chatbot_build_graph(self):

        self.basic_chatbot_node = basicChatbotNode(self.llm)

        self.graph_builder.add_node("chatBot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatBot")
        self.graph_builder.add_edge("chatBot",END)

        return self.graph_builder.compile()


    def set_use_case(self,usecase):
        if usecase == "Basic Chatbot":
            return self.basic_chatbot_build_graph()
        else:
            raise ValueError("Invalid use case")