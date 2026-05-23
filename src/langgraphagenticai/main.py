import streamlit as st
from src.langgraphagenticai.frontend.streamLitUi.loadUi import LoadUi
from src.langgraphagenticai.llms.groqLLM import GroqLLM
from src.langgraphagenticai.graph.graphBuilder import GraphBuilder
from src.langgraphagenticai.frontend.streamLitUi.displayResult import DisplayResultStreamlit

def load_langgrap_Agentic_api():

    ##load ui
    ui = LoadUi()
    userControls = ui.load_ui()

    if not userControls:
        st.error("Please select the option in the sidebar")
        return 

    user_message = st.chat_input("Enter your message")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=userControls)
            llm_model = obj_llm_config.get_llm_model()
            if not llm_model:
                st.error("Error: LLM model could not be initialised")
                return
            
            usecase = userControls.get("usecase")

            if not usecase:
                st.error("Error: Use case is not selected")
                return
            

            graph_builder = GraphBuilder(llm_model)
            try:
                graph = graph_builder.set_use_case(usecase)
                display = DisplayResultStreamlit(usecase,graph,user_message)
                display.display_result()
                if not graph:
                    st.error("Error: Graph could not be initialised")
                    return
                
            except Exception as e:
                st.error(f"Error: {e}")
                return
                
        except Exception as e:
            st.error(f"Error: {e}")
            return


    
    