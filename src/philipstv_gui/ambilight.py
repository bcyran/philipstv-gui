import tkinter as tk
from enum import Enum
from functools import partial
from tkinter import Button as LegacyButton
from typing import Any, Dict, Optional, Tuple

import ttkbootstrap as ttk
from philipstv import AmbilightColor, PhilipsTVRemote
from ttkbootstrap.colorutils import color_to_hex, contrast_color
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from ttkbootstrap.tooltip import ToolTip

from philipstv_gui.errors import handle_remote_errors


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
            container, autostyle=False, relief=tk.FLAT, **kwargs
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
        self.refresh()

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        settings_frame = ttk.Labelframe(self, text="Settings")
        settings_frame.grid(row=0, column=0, sticky=tk.EW, padx=2, pady=2)

        self._power_toggle = ttk.Checkbutton(
            settings_frame,
            text="Ambilight enabled",
            bootstyle="round-toggle",
            command=self._toggle_power,
        )
        self._power_toggle.pack(fill=tk.BOTH, padx=2, pady=2)

        self._lock_toggle = ttk.Checkbutton(
            settings_frame, text="Same color on all sides", bootstyle="round-toggle"
        )
        self._lock_toggle.pack(fill=tk.BOTH, padx=2, pady=2)

        colors_frame = ttk.Labelframe(self, text="Colors")
        colors_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=2, pady=2)

        for side in AmbilightSide:
            button = ColorButton(
                colors_frame,
                command=partial(self._select_color, side),
                text=side.value.capitalize(),
            )
            button.pack(fill=tk.BOTH, padx=2, pady=2)
            ToolTip(button, text="Click to adjust")
            self._color_buttons[side] = button

        self.grid()

    def refresh(self) -> None:
        if not (self.remote and self.remote.auth):
            return
        with handle_remote_errors(self):
            self._ambilight_enabled = self.remote.get_ambilight_power()

    def _toggle_power(self) -> None:
        if not (self.remote and self.remote.auth):
            return
        with handle_remote_errors(self):
            self.remote.set_ambilight_power(self._ambilight_enabled)
        if self._ambilight_enabled:
            self._apply_colors()

    def _select_color(self, selected_side: AmbilightSide) -> None:
        color_chooser = ColorChooserDialog()
        color_chooser.show()
        color = color_chooser.result
        if not color:
            return
        sides_to_set = {selected_side} if not self._sides_locked else set(AmbilightSide)
        for side in sides_to_set:
            self._set_side_color(side, color.rgb)
        self._apply_colors()

    def _set_side_color(self, side: AmbilightSide, color: Color) -> None:
        self._colors[side] = color
        self._color_buttons[side].set_color(color)

    def _apply_colors(self) -> None:
        if not (self.remote and self.remote.auth):
            return
        if not self._ambilight_enabled:
            return
        ambilight_values = {
            side.value: AmbilightColor.from_tuple(color) for side, color in self._colors.items()
        }
        with handle_remote_errors(self):
            self.remote.set_ambilight_color(**ambilight_values)

    @property
    def _ambilight_enabled(self) -> bool:
        return "selected" in self._power_toggle.state()

    @_ambilight_enabled.setter
    def _ambilight_enabled(self, state: bool) -> None:
        self._power_toggle.state(["selected"] if state else [])

    @property
    def _sides_locked(self) -> bool:
        return "selected" in self._lock_toggle.state()

    @_sides_locked.setter
    def _sides_locked(self, state: bool) -> None:
        self._lock_toggle.state(["selected"] if state else [])
