import logging
import logging.handlers
from python_reactive_ui.backends.gtk3 import create_root
from python_reactive_ui.backends.gtk3.builtin import Box
from python_reactive_ui.backends.gtk3.builtin import Label
from python_reactive_ui.backends.gtk3.builtin import Button
from python_reactive_ui.backends.gtk3.builtin import ProgressBar
from python_reactive_ui.backends.gtk3.builtin.blackbox import BlackBox
from python_reactive_ui import (
    Children,
    Props,
    use_state,
    Component,
)

# fmt: off
import gi

from python_reactive_ui.lib.hooks import use_effect

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on

testlabel = Gtk.Label.new("blackbox")


class Incremental(Component):
    def _render(self, props: Props, children: Children):
        counter, set_counter = use_state(self, 0)
        use_effect(self, lambda: print("Ayoooo"), [counter == 3])

        box_children = [
            Button(
                {
                    "on_click": lambda _: set_counter(counter + 1),
                    "vexpand": counter % 2 == True,
                },
                [Label({"text": "+1"})],
            ),
            Label(
                {"text": f"Counted {counter} clicks", "css_classes": ["test-class"]},
            ),
            ProgressBar({"fraction": counter / 50}),
            # BlackBox({}, widget=testlabel),
        ]

        if counter > 5 and counter < 10:
            box_children.append(Label({"text": f"Loads of clicks!"}))

        elem = Box({"orientation": "vertical"}, box_children)
        return elem


def test():
    setup_logging()
    root = create_root(Gtk.Window.new(Gtk.WindowType.TOPLEVEL))
    elem = Incremental(dict())
    # elem._print_on_render = True
    root.render(elem)
    Gtk.main()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        style="{",
        format="[{levelname}({name}):{filename}:{funcName}] {message}",
    )
    root_logger = logging.getLogger()
    sys_handler = logging.handlers.SysLogHandler(address="/dev/log")
    root_logger.addHandler(sys_handler)
