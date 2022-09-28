import logging
import logging.handlers
from python_reactive_ui.backends.gtk3.render import create_root
from python_reactive_ui.backends.gtk3.builtin.box import Box
from python_reactive_ui.backends.gtk3.builtin.label import Label
from python_reactive_ui.backends.gtk3.builtin.button import Button
from python_reactive_ui.backends.gtk3.builtin.progress_bar import ProgressBar
from python_reactive_ui.component import (
    Children,
    Props,
    create_element,
    print_tree,
    use_state,
    Component,
)
from typing import List

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Incremental(Component):
    def _render(self, props: Props, children: Children):
        counter, set_counter = use_state(self, 0)

        box_children = [
            create_element(
                Button,
                {"on_click": lambda _: set_counter(counter + 1)},
                [create_element(Label, {"text": "+1"})],
            ),
            create_element(Label, {"text": f"Counted {counter} clicks"}),
            create_element(ProgressBar, {"fraction": counter / 50}),
        ]

        if counter > 5 and counter < 10:
            box_children.append(create_element(Label, {"text": f"Loads of clicks!"}))

        elem = create_element(Box, {"orientation": "vertical"}, box_children)
        return elem


def test():
    setup_logging()
    root = create_root(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
    elem = create_element(Incremental, dict())
    elem._print_on_render = True
    root.render(elem)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="[{levelname}({name}):{filename}:{funcName}] {message}",
    )
    root_logger = logging.getLogger()
    sys_handler = logging.handlers.SysLogHandler(address="/dev/log")
    root_logger.addHandler(sys_handler)
