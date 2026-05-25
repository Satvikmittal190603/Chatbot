import streamlit as st
import os
from src.langgraphagenticai.frontend.streamLitUi.loadUi import LoadUi
from src.langgraphagenticai.llms.groqLLM import GroqLLM
from src.langgraphagenticai.graph.graphBuilder import GraphBuilder
from src.langgraphagenticai.frontend.streamLitUi.displayResult import DisplayResultStreamlit

from langgraph.checkpoint.memory import MemorySaver

def load_langgrap_Agentic_api():

    if "checkpointer" not in st.session_state:
        st.session_state.checkpointer = MemorySaver()
    if "thread_id" not in st.session_state:
        import uuid
        st.session_state.thread_id = str(uuid.uuid4())

    ##load ui
    ui = LoadUi()
    userControls = ui.load_ui()

    if not userControls:
        st.error("Please select the option in the sidebar")
        return 

    if userControls.get("TAVILY_API_KEY"):
        
        os.environ["TAVILY_API_KEY"] = userControls["TAVILY_API_KEY"]

    if st.session_state.get("isFetchButtonClicked"):
        user_message = st.session_state.time_frame
        st.session_state.isFetchButtonClicked = False
    else:
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
            

            graph_builder = GraphBuilder(llm_model, checkpointer=st.session_state.checkpointer)
            try:
                graph = graph_builder.set_use_case(usecase)
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                display = DisplayResultStreamlit(usecase,graph,user_message,config=config)
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


    
    