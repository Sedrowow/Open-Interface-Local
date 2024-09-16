# app/models/ollama_model.py
import json
from typing import Any, Dict
import ollama
from models.model import Model

class OllamaModel(Model):
    def __init__(self, model_name, base_url, context):
        super().__init__(model_name, base_url, context)
        self.model_name = model_name
        self.download_model(model_name)

    def get_instructions_for_objective(self, original_user_request: str, step_num: int = 0) -> Dict[str, Any]:
        formatted_request = self.format_user_request_for_llm(original_user_request, step_num)
        llm_response = self.send_message_to_llm(formatted_request)
        return self.convert_llm_response_to_json_instructions(llm_response)

    def format_user_request_for_llm(self, original_user_request, step_num, screenshot_file_id=None) -> str:
        """
        Formats the user request for the LLM.

        Args:
            original_user_request (str): The original request from the user.
            step_num (int): The step number in the process.
            screenshot_file_id (str, optional): The ID of the screenshot file. Defaults to None.

        Returns:
            str: The formatted request as a JSON string.
        """
        request_data = {
            'original_user_request': original_user_request,
            'step_num': step_num
        }
        if screenshot_file_id:
            request_data['screenshot'] = screenshot_file_id
        return json.dumps(request_data)

    def send_message_to_llm(self, formatted_user_request: str) -> Any:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'context/instructions',
                        'content': self.context
                    },
                    {
                        'role': 'prompt',
                        'content': formatted_user_request
                    },
                     ]
            )
            return response
        except Exception as e:
            print(f'Error while sending message to LLM - {e}')
            return None

    def convert_llm_response_to_json_instructions(self, llm_response: Any) -> dict[str, Any]:
        try:
            if llm_response and 'choices' in llm_response and len(llm_response['choices']) > 0:
                llm_response_data = llm_response['choices'][0]['text'].strip()
            else:
                print('Invalid LLM response format')
                return {}
        except (KeyError, IndexError) as e:
            print(f'Error while accessing LLM response - {e}')
            return {}

        start_index = llm_response_data.find('{')
        end_index = llm_response_data.rfind('}')

        try:
            json_response = json.loads(llm_response_data[start_index:end_index + 1].strip())
        except Exception as e:
            print(f'Error while parsing JSON response - {e}')
            json_response = {}

        return json_response

    def download_model(self, model_name: str):
        # Use ollama-python to download the model
        progress = ollama.pull(model_name)
        return progress

    def switch_model(self, model_name: str):
        # Switch to the downloaded model
        self.model_name = model_name

    def cleanup(self):
        pass