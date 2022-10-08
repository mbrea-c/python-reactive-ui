from python_reactive_ui.backends.gtk3.builtin_component import Gtk3BuiltinComponent
from python_reactive_ui import Children, Props

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class ProgressBar(Gtk3BuiltinComponent):
    def _pre_init(self):
        self._set_widget(Gtk.ProgressBar.new())

    def _mount(self):
        self._mounter(self.gtk_widget)

    def _receive_props(self, new_props: Props):
        super()._receive_props(new_props)
        self.gtk_widget.set_fraction(
            new_props["fraction"] if "fraction" in new_props else 0.5
        )

    def _receive_children(self, new_children: Children):
        pass

    def _dismount_node(self):
        self._dismounter(self.gtk_widget)
