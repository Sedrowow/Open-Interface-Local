# app/ui.py
import threading
import tkinter as tk
import webbrowser
from multiprocessing import Queue
from pathlib import Path
from tkinter import ttk

import speech_recognition as sr
from PIL import Image, ImageTk

from llm import LLM
from utils.settings import Settings
from version import version

def open_link(url) -> None:
    webbrowser.open_new(url)

class UI:
    def __init__(self):
        self.main_window = self.MainWindow()

    def run(self) -> None:
        self.main_window.mainloop()

    def display_current_status(self, text: str):
        self.main_window.update_message(text)

    class AdvancedSettingsWindow(tk.Toplevel):
        """
        Self-contained settings sub-window for the UI
        """

        def __init__(self, parent):
            super().__init__(parent)
            self.title('Advanced Settings')
            self.minsize(300, 300)
            self.create_widgets()
            self.settings = Settings()

            # Populate UI
            settings_dict = self.settings.get_dict()

            if 'base_url' in settings_dict:
                self.base_url_entry.insert(0, settings_dict['base_url'])
            DEFAULT_MODEL_NAME = 'gemma2'
            
            if 'model' in settings_dict:
                self.model_entry.insert(0, settings_dict['model'])
                self.model_var.set(settings_dict.get('model', 'custom'))
            else:
                self.model_entry.insert(0, DEFAULT_MODEL_NAME)
                self.model_var.set(DEFAULT_MODEL_NAME)

        def create_widgets(self) -> None:
            # Radio buttons for model selection
            tk.Label(self, text='Select Model:').pack(pady=10, padx=10)
            self.model_var = tk.StringVar(value='custom')  # default selection

            # Create a frame to hold the radio buttons
            radio_frame = ttk.Frame(self)
            radio_frame.pack(padx=20, pady=10)  # Add padding around the frame

            models = [
                ('Google Gemma 2 is a high-performing and efficient model (5.4GB)', 'gemma2'),
                ('A lightweight AI model (2.2GB)', 'phi3.5'),
                ('Meta Llama 3: The most capable openly available LLM to date (4.7GB)', 'llama3'),
                ('Custom (Specify Settings Below)', 'custom')
            ]
            for text, value in models:
                ttk.Radiobutton(radio_frame, text=text, value=value, variable=self.model_var).pack(anchor=tk.W)

            label_base_url = tk.Label(self, text='Custom OpenAI-Like API Model Base URL')
            label_base_url.pack(pady=10)

            # Entry for Base URL
            self.base_url_entry = ttk.Entry(self, width=30)
            self.base_url_entry.pack()

            # Model Label
            label_model = tk.Label(self, text='Custom Model Name:')
            label_model.pack(pady=10)

            # Entry for Model
            self.model_entry = ttk.Entry(self, width=30)
            self.model_entry.pack()

            # Save Button
            save_button = ttk.Button(self, text='Save Settings', command=self.save_button)
            save_button.pack(pady=20)

        def save_button(self) -> None:
            base_url = self.base_url_entry.get().strip()
            model = self.model_var.get() if self.model_var.get() != 'custom' else self.model_entry.get().strip()
            settings_dict = {
                'base_url': base_url,
                'model': model,
            }

            self.settings.save_settings_to_file(settings_dict)
            self.destroy()

    class SettingsWindow(tk.Toplevel):
        """
        Self-contained settings sub-window for the UI
        """

        def __init__(self, parent):
            super().__init__(parent)
            self.title('Settings')
            self.minsize(300, 450)
            self.create_widgets()

            self.settings = Settings()

            # Populate UI
            settings_dict = self.settings.get_dict()

            if 'api_key' in settings_dict:
                self.api_key_entry.insert(0, settings_dict['api_key'])
            if 'default_browser' in settings_dict:
                self.browser_combobox.set(settings_dict['default_browser'])
            if 'play_ding_on_completion' in settings_dict:
                self.play_ding.set(1 if settings_dict['play_ding_on_completion'] else 0)
            if 'custom_llm_instructions' in settings_dict:
                self.llm_instructions_text.insert('1.0', settings_dict['custom_llm_instructions'])

        def create_widgets(self) -> None:

            # Label for Browser Choice
            label_browser = tk.Label(self, text='Choose Default Browser:')
            label_browser.pack(pady=10)

            # Dropdown for Browser Choice
            self.browser_var = tk.StringVar()
            self.browser_combobox = ttk.Combobox(self, textvariable=self.browser_var,
                                                 values=['Safari', 'Firefox', 'Chrome'])
            self.browser_combobox.pack(pady=5)
            self.browser_combobox.set('Choose Browser')

            # Label for Custom LLM Instructions
            label_llm = tk.Label(self, text='Custom LLM Instructions:')
            label_llm.pack(pady=10)

            # Text Box for Custom LLM Instructions
            self.llm_instructions_text = tk.Text(self, height=5, width=40)
            self.llm_instructions_text.pack(pady=5)

            # Checkbox for "Play Ding" option
            self.play_ding = tk.IntVar()
            play_ding_checkbox = ttk.Checkbutton(self, text="Play Ding on Completion", variable=self.play_ding)
            play_ding_checkbox.pack(pady=10)

            # Save Button
            save_button = ttk.Button(self, text='Save Settings', command=self.save_button)
            save_button.pack(pady=(10, 0))

            # Button to open Advanced Settings
            advanced_settings_button = ttk.Button(self, text='Advanced Settings', command=self.open_advanced_settings)
            advanced_settings_button.pack(pady=(0, 10))

            # Hyperlink Label
            link_label = tk.Label(self, text='Instructions', fg='#499CE4')
            link_label.pack()
            link_label.bind('<Button-1>', lambda e: open_link(
                'https://github.com/AmberSahdev/Open-Interface?tab=readme-ov-file#setup-%EF%B8%8F'))

            # Check for updates Label
            update_label = tk.Label(self, text='Check for Updates', fg='#499CE4', font=('Helvetica', 10))
            update_label.pack()
            update_label.bind('<Button-1>', lambda e: open_link(
                'https://github.com/AmberSahdev/Open-Interface/releases/latest'))

            # Version Label
            version_label = tk.Label(self, text=f'Version: {str(version)}', font=('Helvetica', 10))
            version_label.pack(side="bottom", pady=10)

        def save_button(self) -> None:
            api_key = self.api_key_entry.get().strip()
            default_browser = self.browser_var.get()
            settings_dict = {
                'api_key': api_key,
                'default_browser': default_browser,
                'play_ding_on_completion': bool(self.play_ding.get()),
                'custom_llm_instructions': self.llm_instructions_text.get("1.0", "end-1c").strip()
            }

            self.settings.save_settings_to_file(settings_dict)
            self.destroy()

        def open_advanced_settings(self):
            # Open the advanced settings window
            UI.AdvancedSettingsWindow(self)

    class MainWindow(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title('Open Interface')
            self.minsize(420, 250)

            # PhotoImage object needs to persist as long as the app does, hence it's a class object.
            path_to_icon_png = Path(__file__).resolve().parent.joinpath('resources', 'icon.png')
            path_to_microphone_png = Path(__file__).resolve().parent.joinpath('resources', 'microphone.png')
            self    .logo_img = ImageTk.PhotoImage(Image.open(path_to_icon_png).resize((50, 50)))
            self.mic_icon = ImageTk.PhotoImage(Image.open(path_to_microphone_png).resize((18, 18)))

            # This adds app icon in linux which pyinstaller can't
            self.tk.call('wm', 'iconphoto', self._w, self.logo_img)

            # MP Queue to facilitate communication between UI and Core.
            # Put user requests received from UI text box into this queue which will then be dequeued in App to be sent
            # to core.
            self.user_request_queue = Queue()

            self.llm = LLM()

            self.model_var = tk.StringVar(value=self.llm.model_name)
            self.create_widgets()

        def on_model_selected(self, event):
           selected_model = self.model_var.get()
           self.llm.switch_model(selected_model)

           # Download the model if not already downloaded
           self.llm.download_model(selected_model)

           # Update the LLM instance with the new model
           self.llm.model_name = selected_model

        def on_submit(self):
           user_request = self.user_input.get("1.0", tk.END).strip()
           if user_request:
                self.user_request_queue.put(user_request)
                # Process the user request with the LLM
                response = self.llm.get_instructions_for_objective(user_request)
                print(response)  # For now, just print the response

if __name__ == "__main__":
    ui = UI()
    ui.run()