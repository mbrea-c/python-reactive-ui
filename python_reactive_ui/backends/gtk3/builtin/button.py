from dataclasses import dataclass
import logging
from typing import Callable, Optional, Tuple, List
from python_reactive_ui.backends.gtk3.render import Gtk3BuiltinComponent
from python_reactive_ui.component import Children, Props

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Button(Gtk3BuiltinComponent):
    def __init__(self):
        super().__init__()
        self.gtk_widget = Gtk.Button.new()
        self.signal_handlers = dict()

    def _receive_props(self, new_props: Props):
        self._update_on_click(
            new_props["on_click"] if "on_click" in new_props else None
        )
        self._props = new_props

    def _receive_children(self, new_children: Children):
        if len(new_children) > 1:
            raise ValueError("button only supports a single child")
        actions = self._compare_children(self._children, new_children)
        self._perform_actions(actions, self.gtk_widget.add, self.gtk_widget.remove)

    def _update_on_click(self, on_click: Optional[Callable]):
        if "clicked" in self.signal_handlers:
            self.gtk_widget.disconnect(self.signal_handlers["clicked"])
            self.signal_handlers.pop("clicked")
        if on_click:
            self.signal_handlers["clicked"] = self.gtk_widget.connect(
                "clicked", on_click
            )

    def _dismount(self):
        self._dismounter(self.gtk_widget)

    def _mount(self):
        self._mounter(self.gtk_widget)
