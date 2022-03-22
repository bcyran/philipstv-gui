import tkinter as tk
from typing import Any, List, Optional

import ttkbootstrap as ttk
from philipstv.remote import PhilipsTVRemote


class Channels(ttk.Frame):  # type: ignore[misc]
    def __init__(self, container: ttk.Frame, remote: Optional[PhilipsTVRemote]) -> None:
        super().__init__(container)

        self.remote = remote
        self._channels_list: List[str] = []

        self._init_widgets()
        self.refresh()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._listbox_values = tk.StringVar()
        self._listbox = tk.Listbox(self, listvariable=self._listbox_values)
        self._listbox.grid(row=0, column=0, sticky=tk.NSEW)
        self._listbox.bind("<<ListboxSelect>>", self._on_selected)

        self.grid()

    def refresh(self) -> None:
        if not self.remote or not self.remote.auth:
            return
        channels_map = self.remote.get_all_channels()
        channels_labels = [f"{num}. {name}" for num, name in channels_map.items()]
        self._channels_list = list(channels_map.values())
        self._listbox_values.set(channels_labels)  # type: ignore[arg-type]

    def _on_selected(self, _: Any) -> None:
        if not self.remote:
            return
        if not (selection := self._listbox.curselection()):  # type: ignore[no-untyped-call]
            return
        selected_channel = self._channels_list[selection[0]]
        self.remote.set_channel(selected_channel)
