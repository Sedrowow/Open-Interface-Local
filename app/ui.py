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
    def __init__(self, root):
        self.root = root
        self.root.title(f"LLM Interface - v{version}")

        self.llm = LLM()

        self.model_var = tk.StringVar(value=self.llm.model_name)
        self.create_widgets()

    def create_widgets(self):
        # Create dropdown for model selection
        model_label = tk.Label(self.root, text="Select Model:")
        model_label.pack()

        model_dropdown = ttk.Combobox(self.root, textvariable=self.model_var)
        model_dropdown['values'] = ('llama3.1', 'phi3', 'gemma2', 'minicpm-v', 'llava', 'mistral-nemo')
        model_dropdown.pack()

        model_dropdown.bind("<<ComboboxSelected>>", self.on_model_selected)

        # Other UI components...

    def on_model_selected(self, event):
        selected_model = self.model_var.get()
        self.llm.switch_model(selected_model)

        # Download the model if not already downloaded
        self.llm.download_model(selected_model)

        # Update the LLM instance with the new model
        self.llm.model_name = selected_model

    # Other methods...

if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()