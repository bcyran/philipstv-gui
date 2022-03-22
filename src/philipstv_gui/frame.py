import tkinter as tk
from typing import Any, Optional

import ttkbootstrap as ttk
from philipstv import PhilipsTVRemote
from philipstv.exceptions import PhilipsTVPairingError
from ttkbootstrap.dialogs.dialogs import Messagebox, Querybox

from philipstv_gui.applications import Applications
from philipstv_gui.channels import Channels
from philipstv_gui.connector import Connector

from .remote import Remote
from .storage import AppData, HostData


class AppFrame(ttk.Frame):  # type: ignore[misc]
    def __init__(self, container: tk.Tk, store: AppData) -> None:
        super().__init__(container)

        self._store: AppData = store
        self._remote: Optional[PhilipsTVRemote] = None

        self._init_widgets()

        if last_host := self._store.last_host:
            self._remote = PhilipsTVRemote.new(last_host.host, (last_host.id, last_host.key))
            self.refresh()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self._connector_panel = Connector(self)
        self._connector_panel.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=5)
        self._connector_panel.bind("<<Pair>>", self._on_pair)
        self._connector_panel.bind("<<Input>>", self._on_input)

        notebook = ttk.Notebook(self)
        notebook.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self._remote_panel = Remote(notebook, self._remote)
        notebook.add(self._remote_panel, text="Remote")

        self._channels_panel = Channels(notebook, self._remote)
        notebook.add(self._channels_panel, text="Channels")

        self._apps_panel = Applications(notebook, self._remote)
        notebook.add(self._apps_panel, text="Apps")

        self.grid()

    def refresh(self) -> None:
        self._remote_panel.remote = self._remote
        self._channels_panel.remote = self._remote
        self._apps_panel.remote = self._remote

        if self._remote:
            self._connector_panel.host_ip = self._remote.host
            self._connector_panel.enabled = not bool(self._remote.auth)

        self._channels_panel.refresh()
        self._apps_panel.refresh()

    def _on_pair(self, _: Any) -> None:
        if not self._connector_panel.host_ip:
            Messagebox.show_error("Enter the IP address!", "Pairing error", parent=self)
            return

        remote = PhilipsTVRemote.new(self._connector_panel.host_ip)

        try:
            credentials = remote.pair(self._ask_for_pin)
        except PhilipsTVPairingError as exc:
            Messagebox.show_error(str(exc), "Pairing error", parent=self)
            return
        else:
            self._remote = remote
        finally:
            self.refresh()

        self._store.last_host = HostData(remote.host, *credentials)
        self._store.save()

    def _on_input(self, _: Any) -> None:
        input_same_as_current = self._remote and self._remote.host == self._connector_panel.host_ip
        self._connector_panel.enabled = not input_same_as_current

    def _ask_for_pin(self) -> str:
        return Querybox.get_string(  # type: ignore[no-any-return]
            "Enther PIN number displayed on the TV", "PIN", parent=self
        )
