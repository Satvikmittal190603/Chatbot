from configparser import ConfigParser

class Uiconfig:
    def __init__(self,config_path="./src/langgraphagenticai/frontend/uiConfigFile.ini"):
        self.config = ConfigParser()
        self.config.read(config_path)

    
    def get_page_title(self):
        return self.config['DEFAULT']['PAGE_TITLE']

    def get_llm_options(self):
        return self.config['DEFAULT']['LLM_OPTIONS'].split(',')

    def get_usecase_options(self):
        return self.config['DEFAULT']['USECASE_OPTIONS'].split(',')

    def get_groq_model_options(self):
        return self.config['DEFAULT']['GROQ_MODEL_OPTIONS'].split(',')

    