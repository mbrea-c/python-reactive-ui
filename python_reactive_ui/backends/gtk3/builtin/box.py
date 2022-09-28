from dataclasses import dataclass
from python_reactive_ui.backends.gtk3.render import Gtk3BuiltinComponent
from python_reactive_ui.component import Children, Component, Props
from typing import List

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Box(Gtk3BuiltinComponent):
    def __init__(self):
        super().__init__()
        self.gtk_widget = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)

    def _receive_props(self, new_props: Props):
        self._update_orientation(
            new_props["orientation"] if "orientation" in new_props else "horizontal",
        )
        self.gtk_widget.set_spacing(
            new_props["spacing"] if "spacing" in new_props else 0
        )

        self._props = new_props

    def _receive_children(self, new_children: Children):
        actions = self._compare_children(self._children, new_children)
        self._perform_actions(actions, self.gtk_widget.add, self.gtk_widget.remove)
        self.gtk_widget.show_all()

    def _update_orientation(self, orientation: str):
        match orientation:
            case "horizontal":
                self.gtk_widget.set_orientation(Gtk.Orientation.HORIZONTAL)
            case "vertical":
                self.gtk_widget.set_orientation(Gtk.Orientation.VERTICAL)
            case other:
                raise ValueError(f"orientation value of {other} is not supported")

    def _mount(self):
        assert isinstance(self._props, Props)
        self._mounter(self.gtk_widget)
        self.gtk_widget.show_all()

    def _dismount(self):
        self._dismounter(self.gtk_widget)
