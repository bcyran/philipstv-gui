import tkinter as tk
from typing import Any, List, Optional

import ttkbootstrap as ttk
from philipstv.remote import PhilipsTVRemote

from philipstv_gui.errors import handle_remote_errors, not_paired_error


class Applications(ttk.Frame):  # type: ignore[misc]
    def __init__(self, container: ttk.Frame, remote: Optional[PhilipsTVRemote]) -> None:
        super().__init__(container)

        self.remote = remote
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
        if not (self.remote and self.remote.auth):
            return
        with handle_remote_errors(self):
            self._apps_list = self.remote.get_applications()
            self._listbox_values.set(self._apps_list)  # type: ignore[arg-type]

    def _on_selected(self, _: Any) -> None:
        if not self.remote:
            not_paired_error(self)
        elif selection := self._listbox.curselection():  # type: ignore[no-untyped-call]
            selected_application = self._apps_list[selection[0]]
            with handle_remote_errors(self):
                self.remote.launch_application(selected_application)
