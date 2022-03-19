import tkinter as tk
from typing import Any, List, Optional

import ttkbootstrap as ttk
from philipstv.remote import PhilipsTVRemote


class Channels(ttk.Frame):  # type: ignore[misc]
    def __init__(self, container: ttk.Frame, remote: Optional[PhilipsTVRemote]) -> None:
        super().__init__(container)

        self._remote = remote
        self._channels_list: List[str] = []

        self._init_widgets()
        self._populate_channels()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._listbox_values = tk.StringVar()
        self._listbox = tk.Listbox(self, listvariable=self._listbox_values)
        self._listbox.grid(row=0, column=0, sticky=tk.NSEW)
        self._listbox.bind("<<ListboxSelect>>", self._on_selected)

        self.grid()

    def _populate_channels(self) -> None:
        if not self._remote:
            return
        channels_map = self._remote.get_all_channels()
        channels_labels = [f"{num}. {name}" for num, name in channels_map.items()]
        self._channels_list = list(channels_map.values())
        self._listbox_values.set(channels_labels)  # type: ignore[arg-type]

    def _on_selected(self, _: Any) -> None:
        if not self._remote:
            return
        if not (selection := self._listbox.curselection()):  # type: ignore[no-untyped-call]
            return
        selected_channel = self._channels_list[selection[0]]
        self._remote.set_channel(selected_channel)

    @property
    def remote(self) -> Optional[PhilipsTVRemote]:
        return self._remote

    @remote.setter
    def remote(self, value: Optional[PhilipsTVRemote]) -> None:
        self._remote = value
        self._populate_channels()
