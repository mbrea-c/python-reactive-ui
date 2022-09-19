import logging
import logging.handlers
from pyact.backends.gtk3 import create_root
from pyact.backends.gtk3.builtin.box import Box, BoxProps
from pyact.backends.gtk3.builtin.label import Label, LabelProps
from pyact.backends.gtk3.builtin.button import Button, ButtonProps
from pyact.component import Element, Props, createElement, print_tree, use_state
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def Incremental(element: Element, props: Props):
    counter, set_counter = use_state(element, 0)

    elem = createElement(
        Box,
        BoxProps(orientation="vertical"),
        [
            createElement(
                Button,
                ButtonProps(on_click=lambda _: set_counter(counter + 1)),
                [createElement(Label, LabelProps(text="+1"))],
            ),
            createElement(Label, LabelProps(text=f"Counted {counter} clicks")),
        ],
    )
    print_tree(elem)
    return elem


def test():
    setup_logging()
    root = create_root(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
    root.render(createElement(Incremental, Props()))


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="[{levelname}({name}):{filename}:{funcName}] {message}",
    )
    root_logger = logging.getLogger()
    sys_handler = logging.handlers.SysLogHandler(address="/dev/log")
    root_logger.addHandler(sys_handler)
