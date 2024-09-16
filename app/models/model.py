import os
from typing import Any


class Model:
    def __init__(self, model_name, base_url, context):
        self.model_name = model_name
        self.base_url = base_url
        self.context = context


    def get_instructions_for_objective(self, *args) -> dict[str, Any]:
        pass

    def format_user_request_for_llm(self, *args):
        pass

    def convert_llm_response_to_json_instructions(self, *args) -> dict[str, Any]:
        pass

    def cleanup(self, *args):
        pass
