import tkinter as tk
from tkinter import ttk
from typing import Any


class Connector(ttk.Frame):
    def __init__(self, container: ttk.Frame) -> None:
        super().__init__(container)

        self._init_widgets()

    def _init_widgets(self) -> None:
        self._host_ip = tk.StringVar(self)
        self._host_ip.trace_add("write", self._on_input)

        self._ip_input = ttk.Entry(self, textvariable=self._host_ip)
        self._ip_input.pack(fill="x")

        self._pair_button = ttk.Button(self, text="pair", command=self._on_pair)
        self._pair_button.pack(fill="x")

        self.pack()

    def _on_input(self, *_: Any) -> None:
        self.event_generate("<<Input>>")

    def _on_pair(self) -> None:
        self.event_generate("<<Pair>>")

    @property
    def host_ip(self) -> str:
        return self._host_ip.get()

    @host_ip.setter
    def host_ip(self, value: str) -> None:
        self._host_ip.set(value)

    @property
    def enabled(self) -> bool:
        return bool(self._pair_button["state"] == "normal")

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._pair_button["state"] = "normal" if value else "disabled"
