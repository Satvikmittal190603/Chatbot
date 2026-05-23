import json

class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result(self):
        if self.usecase == "basic_chatbot":
           for event in self.graph.stream({"messages": [{"role": "user", "content": self.user_message}]}):
               print(event.values())
               for value in event.values():
                print(value['messages'])
                with st.chat_message("user"):
                    st.write(self.user_message)
                with st.chat_message("assistant"):
                    st.write(value['messages'][-1].content)