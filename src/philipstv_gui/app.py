import tkinter as tk
from tkinter import font

from ttkbootstrap.window import Window

from .frame import AppFrame
from .storage import AppData


class App(Window):  # type: ignore
    def __init__(self) -> None:
        super().__init__(title="PhilipsTV GUI")

        font.nametofont("TkDefaultFont").config(size=11)
        font.nametofont("TkTextFont").config(size=11)

        self._app_data = AppData.load()

        self._init_widgets()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        AppFrame(self, self._app_data).grid(row=0, column=0, sticky=tk.NSEW)

        self.grid()
