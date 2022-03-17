import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional

from philipstv.remote import PhilipsTVRemote


class Applications(ttk.Frame):
    def __init__(self, container: ttk.Widget, remote: Optional[PhilipsTVRemote]) -> None:
        super().__init__(container)

        self._remote = remote
        self._apps_list: List[str] = []

        self._init_widgets()
        self._populate_apps()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._listbox_values = tk.StringVar()
        self._listbox = tk.Listbox(self, listvariable=self._listbox_values)
        self._listbox.grid(row=0, column=0, sticky=tk.NSEW)
        self._listbox.bind("<<ListboxSelect>>", self._on_selected)

        self.grid()

    def _populate_apps(self) -> None:
        if not self._remote:
            return
        self._apps_list = self._remote.get_applications()
        self._listbox_values.set(self._apps_list)  # type: ignore[arg-type]

    def _on_selected(self, _: Any) -> None:
        if not self._remote:
            return
        selected_index = self._listbox.curselection()[0]  # type: ignore[no-untyped-call]
        selected_application = self._apps_list[selected_index]
        self._remote.launch_application(selected_application)

    @property
    def remote(self) -> Optional[PhilipsTVRemote]:
        return self._remote

    @remote.setter
    def remote(self, value: Optional[PhilipsTVRemote]) -> None:
        self._remote = value
        self._populate_apps()
