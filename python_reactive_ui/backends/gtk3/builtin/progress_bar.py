from dataclasses import dataclass
from python_reactive_ui.backends.gtk3.render import Gtk3BuiltinComponent
from python_reactive_ui.component import Children, Props

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class ProgressBar(Gtk3BuiltinComponent):
    def __init__(self):
        super().__init__()
        self.gtk_widget = Gtk.ProgressBar.new()

    def _mount(self):
        self._mounter(self.gtk_widget)
        self.gtk_widget.show_all()

    def _receive_props(self, new_props: Props):
        self.gtk_widget.set_fraction(
            new_props["fraction"] if "fraction" in new_props else 0.5
        )
        self._props = new_props

    def _receive_children(self, new_children: Children):
        pass

    def _dismount_node(self):
        self._dismounter(self.gtk_widget)
