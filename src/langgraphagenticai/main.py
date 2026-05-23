import streamlit as st
from src.langgraphagenticai.frontend.streamLitUi.loadUi import LoadUi

def load_langgrap_Agentic_api():

    ##load ui
    ui = LoadUi()
    userControls = ui.load_ui()

    if not userControls:
        st.error("Please select the option in the sidebar")
        return 

    user_message = st.chat_input("Enter your message")



    
    