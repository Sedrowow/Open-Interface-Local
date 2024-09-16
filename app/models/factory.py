from models.ollama_model import OllamaModel

class ModelFactory:
    @staticmethod
    def create_model(model_name, *args):
        if model_name == 'ollama':
            return OllamaModel(model_name, *args)
        else:
            raise ValueError(f'Unsupported model type {model_name}. Create entry in app/models/')