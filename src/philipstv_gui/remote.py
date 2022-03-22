import tkinter as tk
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, List, Optional

import ttkbootstrap as ttk
from philipstv import PhilipsTVRemote
from philipstv.model import InputKeyValue
from ttkbootstrap.dialogs.dialogs import Messagebox

ButtonCallback = Callable[[InputKeyValue], None]


@dataclass(frozen=True)
class RemoteButton:
    row: int
    column: int
    label: str
    value: InputKeyValue
    keys: List[str] = field(default_factory=list)
    rowspan: int = 1
    colspan: int = 1

    def install(
        self,
        container: ttk.Frame,
        click_callback: ButtonCallback,
        key_callback: ButtonCallback,
    ) -> ttk.Button:
        button = ttk.Button(
            container,
            text=self.label,
            command=partial(click_callback, self.value),
            bootstyle="dark-outline",
        )
        button.grid(
            row=self.row,
            column=self.column,
            rowspan=self.rowspan,
            columnspan=self.colspan,
            sticky=tk.NSEW,
            padx=1,
            pady=1,
        )
        for key in self.keys:
            container.bind_all(f"<Key-{key}>", partial(key_callback, self.value))
        return button


BUTTONS = [
    RemoteButton(0, 0, "power", InputKeyValue.STANDBY, colspan=3),
    RemoteButton(1, 0, "ambilight", InputKeyValue.AMBILIGHT_ON_OFF, colspan=3),
    RemoteButton(2, 0, "adjust", InputKeyValue.ADJUST),
    RemoteButton(2, 1, "tv", InputKeyValue.WATCH_TV, ["t"]),
    RemoteButton(2, 2, "source", InputKeyValue.SOURCE, ["i"]),
    RemoteButton(3, 1, "up", InputKeyValue.CURSOR_UP, ["Up", "w"]),
    RemoteButton(4, 0, "left", InputKeyValue.CURSOR_LEFT, ["Left", "a"]),
    RemoteButton(4, 1, "ok", InputKeyValue.CONFIRM, ["Return"]),
    RemoteButton(4, 2, "right", InputKeyValue.CURSOR_RIGHT, ["Right", "d"]),
    RemoteButton(5, 1, "down", InputKeyValue.CURSOR_DOWN, ["Down", "s"]),
    RemoteButton(6, 0, "back", InputKeyValue.BACK, ["BackSpace", "Escape"]),
    RemoteButton(6, 1, "home", InputKeyValue.HOME, ["Home", "h"]),
    RemoteButton(6, 2, "options", InputKeyValue.OPTIONS, ["o"]),
    RemoteButton(7, 0, "rewind", InputKeyValue.REWIND, ["bracketleft"]),
    RemoteButton(7, 1, "play", InputKeyValue.PLAY_PAUSE, ["space"]),
    RemoteButton(7, 2, "forward", InputKeyValue.FAST_FORWARD, ["bracketright"]),
    RemoteButton(8, 0, "stop", InputKeyValue.STOP),
    RemoteButton(8, 1, "pause", InputKeyValue.PAUSE, ["p"]),
    RemoteButton(8, 2, "record", InputKeyValue.RECORD, ["r"]),
    RemoteButton(9, 0, "vol+", InputKeyValue.VOLUME_UP, ["plus"]),
    RemoteButton(9, 1, "info", InputKeyValue.INFO, ["question"]),
    RemoteButton(9, 2, "ch+", InputKeyValue.CHANNEL_STEP_UP, ["Prior"]),
    RemoteButton(10, 0, "vol-", InputKeyValue.VOLUME_DOWN, ["minus"]),
    RemoteButton(10, 1, "mute", InputKeyValue.MUTE, ["m"]),
    RemoteButton(10, 2, "ch-", InputKeyValue.CHANNEL_STEP_DOWN, ["Next"]),
    RemoteButton(11, 0, "1", InputKeyValue.DIGIT_1, ["1"]),
    RemoteButton(11, 1, "2", InputKeyValue.DIGIT_2, ["2"]),
    RemoteButton(11, 2, "3", InputKeyValue.DIGIT_3, ["3"]),
    RemoteButton(12, 0, "4", InputKeyValue.DIGIT_4, ["4"]),
    RemoteButton(12, 1, "5", InputKeyValue.DIGIT_5, ["5"]),
    RemoteButton(12, 2, "6", InputKeyValue.DIGIT_6, ["6"]),
    RemoteButton(13, 0, "7", InputKeyValue.DIGIT_7, ["7"]),
    RemoteButton(13, 1, "8", InputKeyValue.DIGIT_8, ["8"]),
    RemoteButton(13, 2, "9", InputKeyValue.DIGIT_9, ["9"]),
    RemoteButton(14, 0, "text", InputKeyValue.TELETEXT),
    RemoteButton(14, 1, "0", InputKeyValue.DIGIT_0, ["0"]),
    RemoteButton(14, 2, "subtitle", InputKeyValue.SUBTITLE),
]


class Remote(ttk.Frame):  # type: ignore
    def __init__(self, container: ttk.Frame, remote: Optional[PhilipsTVRemote] = None) -> None:
        super().__init__(container)

        self.remote = remote

        self._init_widgets()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        for row in set(map(lambda button: button.row, BUTTONS)):
            self.rowconfigure(row, weight=1)

        for button in BUTTONS:
            button.install(self, self._button_click, self._button_keypress)

        row += 1
        sep = ttk.Separator(self)
        sep.grid(row=row, column=0, columnspan=3, sticky=tk.NSEW, padx=1, pady=(1, 5))

        row += 1
        self._cap_toggle = ttk.Checkbutton(self, text="Capture keyboard", bootstyle="round-toggle")
        self._cap_toggle.grid(row=row, column=0, columnspan=3, sticky=tk.NSEW, padx=1, pady=(1, 5))

        self.grid()

    def _button_click(self, key: InputKeyValue) -> None:
        self._send_key(key)

    def _button_keypress(self, key: InputKeyValue, *_: Any) -> None:
        if "selected" in self._cap_toggle.state():
            self._send_key(key)

    def _send_key(self, key: InputKeyValue) -> None:
        if not self.remote or not self.remote.auth:
            Messagebox.show_error("First pair with the TV!", "TV error", parent=self)
            return
        self.remote.input_key(key)
