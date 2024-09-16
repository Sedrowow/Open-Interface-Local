# tests/test_llm.py

import unittest
from unittest.mock import patch, MagicMock
from app.llm import LLM
from app.utils.settings import Settings

class TestLLMWithOllama(unittest.TestCase):
    @patch('app.llm.ollama.generate')
    @patch.object(Settings, 'get_dict', return_value={
        'model': 'ollama',
        'base_url': 'http://localhost:8000/'
    })
    def test_llm_with_ollama_model(self, mock_get_dict, mock_generate):
        # Mock the response from ollama.generate
        mock_generate.return_value = {
            'choices': [
                {'text': '{"steps": [{"function": "test_function", "parameters": {"key1": "value1"}, "human_readable_justification": "test justification"}], "done": null}'}
            ]
        }

        # Initialize the LLM class
        llm = LLM()

        # Test the get_instructions_for_objective method
        original_user_request = "Test request"
        step_num = 0
        instructions = llm.get_instructions_for_objective(original_user_request, step_num)

        # Verify the instructions
        expected_instructions = {
            "steps": [
                {
                    "function": "test_function",
                    "parameters": {
                        "key1": "value1"
                    },
                    "human_readable_justification": "test justification"
                }
            ],
            "done": None
        }
        self.assertEqual(instructions, expected_instructions)

        # Verify that ollama.generate was called with the correct parameters
        mock_generate.assert_called_once_with(
            model='ollama',
            prompt='{"original_user_request": "Test request", "step_num": 0}'
        )

    @patch('app.llm.ollama.download')
    def test_download_model(self, mock_download):
        # Initialize the LLM class
        llm = LLM()

        # Test the download_model method
        llm.download_model('ollama')

        # Verify that ollama.download was called with the correct parameters
        mock_download.assert_called_once_with('ollama')

    @patch('app.llm.ollama.generate')
    def test_switch_model(self, mock_generate):
        # Initialize the LLM class
        llm = LLM()

        # Test the switch_model method
        llm.switch_model('other_model_1')

        # Verify that the model name was updated
        self.assertEqual(llm.model_name, 'other_model_1')

if __name__ == '__main__':
    unittest.main()