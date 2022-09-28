from python_reactive_ui.component import (
    BuiltinComponent,
    Component,
    Props,
    Root,
)

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Gtk3Root(Root):
    def __init__(self, root: Gtk.Container):
        self.root = root
        self.tree = None

    def render(self, component: Component):
        component.mount(self.root.add, self.root.remove)
        self.root.show_all()
        Gtk.main()


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


def create_root(root):
    return Gtk3Root(root)
