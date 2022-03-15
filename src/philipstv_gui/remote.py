import tkinter as tk
from dataclasses import dataclass
from functools import partial
from tkinter import ttk
from typing import Callable

from philipstv import PhilipsTVRemote
from philipstv.model import InputKeyValue


@dataclass(frozen=True)
class RemoteButton:
    row: int
    column: int
    text: str
    key: InputKeyValue
    rowspan: int = 1
    colspan: int = 1

    def install(
        self, container: ttk.Frame, callback: Callable[[InputKeyValue], None]
    ) -> ttk.Button:
        button = ttk.Button(container, text=self.text, command=partial(callback, self.key))
        button.grid(
            row=self.row,
            column=self.column,
            rowspan=self.rowspan,
            columnspan=self.colspan,
            sticky=tk.EW,
        )
        return button


BUTTONS = [
    RemoteButton(0, 0, "power", InputKeyValue.STANDBY, colspan=3),
    RemoteButton(1, 0, "ambilight", InputKeyValue.AMBILIGHT_ON_OFF, colspan=3),
    RemoteButton(2, 0, "adjust", InputKeyValue.ADJUST),
    RemoteButton(2, 1, "tv", InputKeyValue.WATCH_TV),
    RemoteButton(2, 2, "source", InputKeyValue.SOURCE),
    RemoteButton(3, 1, "up", InputKeyValue.CURSOR_UP),
    RemoteButton(4, 0, "left", InputKeyValue.CURSOR_LEFT),
    RemoteButton(4, 1, "ok", InputKeyValue.CONFIRM),
    RemoteButton(4, 2, "right", InputKeyValue.CURSOR_RIGHT),
    RemoteButton(5, 1, "down", InputKeyValue.CURSOR_DOWN),
    RemoteButton(6, 0, "back", InputKeyValue.BACK),
    RemoteButton(6, 1, "home", InputKeyValue.HOME),
    RemoteButton(6, 2, "options", InputKeyValue.OPTIONS),
    RemoteButton(7, 0, "rewind", InputKeyValue.REWIND),
    RemoteButton(7, 1, "play", InputKeyValue.PLAY_PAUSE),
    RemoteButton(7, 2, "forward", InputKeyValue.FAST_FORWARD),
    RemoteButton(8, 0, "stop", InputKeyValue.STOP),
    RemoteButton(8, 1, "pause", InputKeyValue.PAUSE),
    RemoteButton(8, 2, "record", InputKeyValue.RECORD),
    RemoteButton(9, 0, "vol+", InputKeyValue.VOLUME_UP),
    RemoteButton(9, 1, "info", InputKeyValue.INFO),
    RemoteButton(9, 2, "ch+", InputKeyValue.CHANNEL_STEP_UP),
    RemoteButton(10, 0, "vol-", InputKeyValue.VOLUME_DOWN),
    RemoteButton(10, 1, "mute", InputKeyValue.MUTE),
    RemoteButton(10, 2, "ch-", InputKeyValue.CHANNEL_STEP_DOWN),
    RemoteButton(11, 0, "1", InputKeyValue.DIGIT_1),
    RemoteButton(11, 1, "2", InputKeyValue.DIGIT_2),
    RemoteButton(11, 2, "3", InputKeyValue.DIGIT_3),
    RemoteButton(12, 0, "4", InputKeyValue.DIGIT_4),
    RemoteButton(12, 1, "5", InputKeyValue.DIGIT_5),
    RemoteButton(12, 2, "6", InputKeyValue.DIGIT_6),
    RemoteButton(13, 0, "7", InputKeyValue.DIGIT_7),
    RemoteButton(13, 1, "8", InputKeyValue.DIGIT_8),
    RemoteButton(13, 2, "9", InputKeyValue.DIGIT_6),
    RemoteButton(14, 0, "text", InputKeyValue.TELETEXT),
    RemoteButton(14, 1, "0", InputKeyValue.DIGIT_0),
    RemoteButton(14, 2, "subtitle", InputKeyValue.SUBTITLE),
]


class Remote(ttk.Frame):
    def __init__(self, container: ttk.Frame, remote: PhilipsTVRemote) -> None:
        super().__init__(container)
        self.remote = remote

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self._init_widgets()
        self.grid()

    def _init_widgets(self) -> None:
        for button in BUTTONS:
            button.install(self, self._key_press)

    def _key_press(self, key: InputKeyValue) -> None:
        self.remote.input_key(key)
