import tkinter as tk
from typing import Any, List, Optional

import ttkbootstrap as ttk
from philipstv.remote import PhilipsTVRemote


class Applications(ttk.Frame):  # type: ignore[misc]
    def __init__(self, container: ttk.Frame, remote: Optional[PhilipsTVRemote]) -> None:
        super().__init__(container)

        self._remote = remote
        self._apps_list: List[str] = []

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
        if not self._remote or not self._remote.auth:
            return
        self._apps_list = self._remote.get_applications()
        self._listbox_values.set(self._apps_list)  # type: ignore[arg-type]

    def _on_selected(self, _: Any) -> None:
        if not self._remote:
            return
        if not (selection := self._listbox.curselection()):  # type: ignore[no-untyped-call]
            return
        selected_application = self._apps_list[selection[0]]
        self._remote.launch_application(selected_application)

    @property
    def remote(self) -> Optional[PhilipsTVRemote]:
        return self._remote

    @remote.setter
    def remote(self, value: Optional[PhilipsTVRemote]) -> None:
        self._remote = value
        self.refresh()
