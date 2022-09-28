from python_reactive_ui import Props
from python_reactive_ui.lib.core import BuiltinComponent

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Gtk3BuiltinComponent(BuiltinComponent):
    def __init__(self, gtk_widget: Gtk.Widget):
        super().__init__()
        self.gtk_widget = gtk_widget

    def _post_mount(self):
        self.gtk_widget.show_all()

    def _receive_props(self, new_props: Props):
        if "css_classes" in new_props:
            new_classes = new_props["css_classes"]
            style_context = self.gtk_widget.get_style_context()
            old_classes = style_context.list_classes()

            for css_class in new_classes:
                if css_class not in old_classes:
                    style_context.add_class(css_class)
            for css_class in old_classes:
                if css_class not in new_classes:
                    print(f"Removing class: {self}, {css_class}")
                    style_context.remove_class(css_class)
