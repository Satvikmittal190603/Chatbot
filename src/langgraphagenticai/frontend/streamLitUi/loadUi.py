import streamlit as st
from src.langgraphagenticai.frontend.uiConfigFile import Uiconfig
import os

class LoadUi:
    def __init__(self):
        self.uiConfig = Uiconfig()
        self.userControls = {}

    def load_ui(self):
        st.title(self.uiConfig.get_page_title())
        st.sidebar.title("Configuration")

        ## LLM selection
        with st.sidebar.expander("Select LLM", expanded=True):
            self.userControls['llm'] = st.selectbox(
                "Choose your LLM",
                self.uiConfig.get_llm_options()
            )
            ## Model Selection
            if self.userControls['llm'] == "Groq":
                self.userControls['groq_model'] = st.selectbox(
                    "Choose your Groq model",
                    self.uiConfig.get_groq_model_options()
                )
                self.userControls['groq_api_key'] = st.session_state['groq_api_key']=st.text_input(
                    "Enter your Groq API key",
                    type="password"
                )
            
            ## use case selection
            self.userControls['usecase'] = st.selectbox(
                "Choose your use case",
                self.uiConfig.get_usecase_options()
            )

        return self.userControls 
