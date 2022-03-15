import tkinter as tk
from tkinter import simpledialog, ttk
from typing import Optional

from philipstv import PhilipsTVRemote

from .remote import Remote
from .storage import AppData, HostData


class AppFrame(ttk.Frame):
    def __init__(self, container: tk.Tk, store: AppData) -> None:
        super().__init__(container)
        self._store: AppData = store
        self._remote = PhilipsTVRemote.new("")

        self._init_widgets()
        self._init_remote()
        self.grid()

    def _init_widgets(self) -> None:
        self._last_host_ip = tk.StringVar(
            self, self._store.last_host.host if self._store.last_host else ""
        )
        self._ip_input = ttk.Entry(self, textvariable=self._last_host_ip)
        self._ip_input.grid(row=0, column=0, sticky=tk.EW)

        self._pair_button = ttk.Button(self, text="pair", command=self._pair_remote)
        self._pair_button.grid(row=1, column=0, sticky=tk.EW)

        self.remote_panel = Remote(self, self._remote)
        self.remote_panel.grid(row=2, column=0)

    def _init_remote(self) -> None:
        entered_ip = self._get_entered_ip()
        last_host = self._store.last_host
        if entered_ip and last_host and entered_ip == last_host.host:
            self._set_remote(PhilipsTVRemote.new(entered_ip, (last_host.id, last_host.key)))
            self._pair_button["state"] = tk.DISABLED
        elif entered_ip:
            self._set_remote(PhilipsTVRemote.new(entered_ip))
            self._pair_button["state"] = tk.ACTIVE

    def _pair_remote(self) -> None:
        self._init_remote()
        if not (entered_ip := self._get_entered_ip()):
            return
        credentials = self._remote.pair(self._ask_for_pin)
        self._store.last_host = HostData(host=entered_ip, id=credentials[0], key=credentials[1])
        self._store.save()

    def _get_entered_ip(self) -> Optional[str]:
        return self._last_host_ip.get().strip() or None

    def _set_remote(self, remote: PhilipsTVRemote) -> None:
        self._remote = remote
        self.remote_panel.remote = remote

    @staticmethod
    def _ask_for_pin() -> str:
        return simpledialog.askstring(title="PIN", prompt="Enter PIN number displayed on the TV")
