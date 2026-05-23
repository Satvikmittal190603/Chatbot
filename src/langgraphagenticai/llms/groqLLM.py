import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):

        try:
            if self.user_controls_input['groq_model'] == "" and os.environ['GROQ_API_KEY']=="":
                raise ValueError("Groq model is not specified")
            model = ChatGroq(
                model=self.user_controls_input['groq_model'],
                groq_api_key=self.user_controls_input['groq_api_key'],
            )
        except Exception as e:
            raise ValueError(f"Error Occurred with Exception:{e}")
            print(f"Error: {e}")


        return model