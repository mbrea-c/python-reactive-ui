from dataclasses import dataclass, field
from typing import Optional
from python_reactive_ui.backends.gtk3.render import Gtk3BuiltinComponent
from python_reactive_ui.component import Children, Props

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Label(Gtk3BuiltinComponent):
    def __init__(self):
        super().__init__()
        self.gtk_widget = Gtk.Label.new("")

    def _receive_props(self, new_props: Props):
        self.gtk_widget.set_text(new_props["text"] if "text" in new_props else "")
        self._props = new_props

    def _receive_children(self, _: Children):
        pass

    def _mount(self):
        self._mounter(self.gtk_widget)
        self.gtk_widget.show_all()

    def _dismount(self):
        self._dismounter(self.gtk_widget)
