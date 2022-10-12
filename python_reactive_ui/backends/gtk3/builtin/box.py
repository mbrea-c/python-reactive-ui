from python_reactive_ui.backends.gtk3.builtin_component import Gtk3BuiltinComponent
from python_reactive_ui import Children, Props

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Box(Gtk3BuiltinComponent):
    def _pre_init(self):
        self._set_widget(Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0))

    def _receive_props(self, new_props: Props):
        super()._receive_props(new_props)
        self.gtk_widget.set_spacing(
            new_props["spacing"] if "spacing" in new_props else 0
        )

    def _receive_children(self, new_children: Children):
        actions = self._compare_children(self._children, new_children)
        self._perform_actions(actions, self.gtk_widget.add, self.gtk_widget.remove)
        self.gtk_widget.show_all()

    def _mount(self):
        self._mounter(self.gtk_widget)

    def _dismount(self):
        self._dismounter(self.gtk_widget)
