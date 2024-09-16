from models.ollama_model import OllamaModel

class ModelFactory:
    @staticmethod
    def create_model(model_name, *args, context):
        if model_name in ['gemma2', 'llama3', 'phi3.5']:
            return OllamaModel(model_name, *args, context)
        else:
            raise ValueError(f'Unsupported model type {model_name}. Create entry in app/models/')