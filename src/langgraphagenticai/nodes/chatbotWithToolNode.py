from src.langgraphagenticai.state.state import state

class chatbot_with_toolsNode:
    def __init__(self,model):
        self.llm = model

    def create_chatbot(self,tools):

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: state):

            return {"messages":[llm_with_tools.invoke(state['messages'])]}

        return chatbot_node

        