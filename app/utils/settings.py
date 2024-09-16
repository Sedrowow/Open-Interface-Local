# app/utils/settings.py

import json
from pathlib import Path

class Settings:
    def __init__(self):
        self.settings_file = Path('settings.json')
        self.settings_dict = self.load_settings()

    def load_settings(self) -> dict:
        if self.settings_file.exists():
            with self.settings_file.open('r') as file:
                return json.load(file)
        else:
            return {}

    def get_dict(self) -> dict:
        return self.settings_dict

    def save_settings(self):
        with self.settings_file.open('w') as file:
            json.dump(self.settings_dict, file, indent=4)

    def set_model(self, model_name: str):
        self.settings_dict['model'] = model_name
        self.save_settings()
