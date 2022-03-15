import tkinter as tk
from pathlib import Path

from .frame import AppFrame
from .storage import AppData

THIS_DIR = Path(__file__).parent


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PhilipsTV GUI")
        self.resizable(False, False)

        self._app_data = AppData.load()

        self._init_widgets()

    def _init_widgets(self) -> None:
        AppFrame(self, self._app_data)
