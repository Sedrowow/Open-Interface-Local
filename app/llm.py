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

class LLM:
    def __init__(self):
        self.settings_dict: dict[str, str] = Settings().get_dict()
        model_name, base_url = self.get_settings_values()

        self.model_name = model_name
        context = self.read_context_txt_file()

        self.model = ModelFactory.create_model(self.model_name, base_url, context)
        client = Client(host='http://localhost:8000')
        response = client.chat(model='llama3.1', messages=[
          {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
        {
            'role': 'assistant',
            'content': 'The sky is blue because of Rayleigh scattering.'
        }
        ])
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
        context = self.read_context_txt_file()
        self.model = ModelFactory.create_model(self.model_name, context)

    def download_model(self, model_name: str):
        if isinstance(self.model, ollama.list):
            self.model.download_model(model_name)

    def read_context_txt_file(self) -> str:
        context_path = Path('resources/context.txt')
        if context_path.exists():
            with context_path.open('r') as file:
                return file.read()
        return ""
    
    def get_instructions_for_objective(self, original_user_request: str, step_num: int = 0) -> dict[str, Any]:
        return self.model.get_instructions_for_objective(original_user_request, step_num)

    def cleanup(self):
        self.model.cleanup()
