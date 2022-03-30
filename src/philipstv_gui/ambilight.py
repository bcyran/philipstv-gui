import tkinter as tk
from enum import Enum
from functools import partial
from tkinter import Button as LegacyButton
from typing import Any, Dict, Optional, Tuple

import ttkbootstrap as ttk
from philipstv import AmbilightColor, PhilipsTVRemote
from ttkbootstrap.colorutils import color_to_hex, contrast_color
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog


class AmbilightSide(Enum):
    LEFT = "left"
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"


Color = Tuple[int, int, int]


DEFAULT_COLOR = (255, 255, 255)


class ColorButton(LegacyButton):
    def __init__(self, container: ttk.Frame, **kwargs: Any) -> None:
        super().__init__(  # type: ignore[call-arg]
            container, autostyle=False, relief=tk.FLAT, text="click to adjust", **kwargs
        )
        self.set_color(DEFAULT_COLOR)

    def set_color(self, color: Color) -> None:
        hex_color = color_to_hex(color)
        contrast_hex_color = contrast_color(color)
        self.configure(
            background=hex_color,
            activebackground=hex_color,
            foreground=contrast_hex_color,
            activeforeground=contrast_hex_color,
        )


class Ambilight(ttk.Frame):  # type: ignore[misc]
    def __init__(self, container: ttk.Frame, remote: Optional[PhilipsTVRemote]) -> None:
        super().__init__(container)

        self.remote = remote

        self._colors: Dict[AmbilightSide, Color] = {side: DEFAULT_COLOR for side in AmbilightSide}
        self._color_buttons: Dict[AmbilightSide, ColorButton] = {}

        self._init_widgets()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)

        row = 0
        for side in AmbilightSide:
            label = ttk.Label(self, text=side.value.capitalize(), anchor="w")
            label.grid(row=row, column=0, sticky=tk.EW, padx=2, pady=2)
            row += 1
            button = ColorButton(self, command=partial(self._select_color, side))
            button.grid(row=row, column=0, sticky=tk.EW, padx=2, pady=2)
            row += 1
            self._color_buttons[side] = button

        self.grid()

    def _select_color(self, side: AmbilightSide) -> None:
        color_chooser = ColorChooserDialog()
        color_chooser.show()
        color = color_chooser.result
        if not color:
            return
        self._colors[side] = color.rgb
        self._color_buttons[side].set_color(color.rgb)
        self._set_colors()

    def _set_colors(self) -> None:
        if not (self.remote and self.remote.auth):
            return
        ambilight_values = {
            side.value: AmbilightColor.from_tuple(color) for side, color in self._colors.items()
        }
        self.remote.set_ambilight_color(**ambilight_values)
