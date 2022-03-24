from contextlib import contextmanager
from typing import Iterator

import ttkbootstrap as ttk
from philipstv.exceptions import PhilipsTVAPIUnauthorizedError, PhilipsTVError
from ttkbootstrap.dialogs.dialogs import Messagebox


def pairing_error(parent: ttk.Frame, exception: Exception) -> None:
    Messagebox.show_error(str(exception), "Pairing error", parent=parent)


def not_paired_error(parent: ttk.Frame) -> None:
    authentication_error(parent)


def authentication_error(parent: ttk.Frame) -> None:
    Messagebox.show_error("First pair with the TV!", "Not authenticated", parent=parent)


def connection_error(parent: ttk.Frame) -> None:
    Messagebox.show_error(
        "Could not connect with the TV. "
        "Make sure the IP address is correct and TV is powered on.",
        "TV connection error",
        parent=parent,
    )


@contextmanager
def handle_remote_errors(parent: ttk.Frame) -> Iterator[None]:
    try:
        yield
    except PhilipsTVAPIUnauthorizedError:
        authentication_error(parent)
    except PhilipsTVError:
        connection_error(parent)
