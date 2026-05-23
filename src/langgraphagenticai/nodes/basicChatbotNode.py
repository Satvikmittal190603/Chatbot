from src.langgraphagenticai.state.state import state

class basicChatbotNode:
    
    def __init__(self,model):
        self.llm = model

    def process(self,state=state)->dict:
        return {"messages": [self.llm.invoke(state['messages'])]}