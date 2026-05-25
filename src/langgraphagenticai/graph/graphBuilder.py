from langgraph.graph import StateGraph, END, START
from src.langgraphagenticai.state.state import state
from src.langgraphagenticai.nodes.basicChatbotNode import basicChatbotNode
from src.langgraphagenticai.tools.searchTool import get_tools,create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode
from src.langgraphagenticai.nodes.chatbotWithToolNode import chatbot_with_toolsNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model,checkpointer):
        self.llm = model
        self.checkpointer = checkpointer
        self.graph_builder = StateGraph(state)

    def basic_chatbot_build_graph(self):

        self.basic_chatbot_node = basicChatbotNode(self.llm)

        self.graph_builder.add_node("chatBot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatBot")
        self.graph_builder.add_edge("chatBot",END)

        return self.graph_builder.compile(checkpointer=self.checkpointer)

    def chatbot_with_tools_build_graph(self):
        tools = get_tools()
        toolNode = create_tool_node(tools)
        self.chatbot_with_tools_node = chatbot_with_toolsNode(self.llm).create_chatbot(tools)

    
        self.graph_builder.add_node("tools",toolNode)
        self.graph_builder.add_node("chatBot",self.chatbot_with_tools_node)


        self.graph_builder.add_edge(START,"chatBot")
        self.graph_builder.add_conditional_edges("chatBot",tools_condition)
        self.graph_builder.add_edge("tools","chatBot")
        self.graph_builder.add_edge("chatBot",END)

        return self.graph_builder.compile(checkpointer=self.checkpointer)



    def ai_news_buider_graph(self):

        ai_news_node = AINewsNode(self.llm)
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_news)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.set_finish_point("save_result")

        return self.graph_builder.compile(checkpointer=self.checkpointer)


    def set_use_case(self,usecase):
        if usecase == "Basic Chatbot":
            return self.basic_chatbot_build_graph()
        elif usecase == "Chatbot with Tools":
            return self.chatbot_with_tools_build_graph()
        elif usecase == "AI News":
            return self.ai_news_buider_graph()
        else:
            raise ValueError("Invalid use case")