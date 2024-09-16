# app/llm.py
from pathlib import Path
from typing import Any
import ollama
from ollama import Client
from models.factory import ModelFactory
from utils import local_info
from utils.screen import Screen
from utils.settings import Settings

DEFAULT_MODEL_NAME = "gemma2"

class LLM(Client):
    def __init__(self):
        self.settings_dict: dict[str, str] = Settings().get_dict()
        model_name, base_url = self.get_settings_values()

        self.model_name = model_name
        context = self.read_context_txt_file()

        self.model = ModelFactory.create_model(self.model_name, base_url, context)
        super().__init__(base_url)  # Correct usage
        
    def get_settings_values(self) -> tuple[str, str]:
        model_name = self.settings_dict.get('model')
        if not model_name:
            model_name = DEFAULT_MODEL_NAME

        base_url = self.settings_dict.get('base_url', '')
        if not base_url:
            base_url = 'http://localhost:8000/'
        base_url = base_url.rstrip('/') + '/'

        return model_name, base_url

    def switch_model(self, model_name: str):
        self.model_name = model_name
        self.model = ModelFactory.create_model(self.model_name)

    def download_model(self, model_name: str):
        if isinstance(self.model, ollama.show(model=model_name)):
            self.model.download_model(model_name)

    def read_context_txt_file(self) -> str:
        # Construct context for the assistant by reading context.txt and adding extra system information
        context = ''
        path_to_context_file = Path(__file__).resolve().parent.joinpath('resources', 'context.txt')
        with open(path_to_context_file, 'r') as file:
            context += file.read()

        context += f' Locally installed apps are {",".join(local_info.locally_installed_apps)}.'
        context += f' OS is {local_info.operating_system}.'
        context += f' Primary screen size is {Screen().get_size()}.\n'

        if 'default_browser' in self.settings_dict.keys() and self.settings_dict['default_browser']:
            context += f'\nDefault browser is {self.settings_dict["default_browser"]}.'

        if 'custom_llm_instructions' in self.settings_dict:
            context += f'\nCustom user-added info: {self.settings_dict["custom_llm_instructions"]}.'

        return context
    
    def get_instructions_for_objective(self, original_user_request: str, step_num: int = 0) -> dict[str, Any]:
        return self.model.get_instructions_for_objective(original_user_request, step_num)

    def cleanup(self):
        self.model.cleanup()
