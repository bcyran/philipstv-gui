import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import Any, Optional, Tuple

from philipstv import PhilipsTVRemote

from philipstv_gui.connector import Connector

from .remote import Remote
from .storage import AppData


class AppFrame(ttk.Frame):
    def __init__(self, container: tk.Tk, store: AppData) -> None:
        super().__init__(container)

        self._store: AppData = store
        self._remote: Optional[PhilipsTVRemote] = None

        self._init_widgets()

        if last_host := self._store.last_host:
            self._init_host(last_host.host, (last_host.id, last_host.key))

    def _init_widgets(self) -> None:
        self._connector_panel = Connector(self)
        self._connector_panel.grid(row=0, column=0, sticky=tk.EW)
        self._connector_panel.bind("<<Pair>>", self._pair)

        self._remote_panel = Remote(self, self._remote)
        self._remote_panel.grid(row=1, column=0, sticky=tk.EW)

        self.grid()

    def _init_host(self, host: str, auth: Optional[Tuple[str, str]] = None) -> PhilipsTVRemote:
        self._remote = PhilipsTVRemote.new(host, auth)
        self._remote_panel.remote = self._remote
        self._connector_panel.host_ip = host
        return self._remote

    def _pair(self, _: Any) -> None:
        if not self._connector_panel.host_ip:
            messagebox.showerror("Pairing error", "First enter the IP address!")
            return
        self._init_host(self._connector_panel.host_ip).pair(self._ask_for_pin)

    @staticmethod
    def _ask_for_pin() -> str:
        return simpledialog.askstring(title="PIN", prompt="Enter PIN number displayed on the TV")
