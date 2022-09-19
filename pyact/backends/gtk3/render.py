from pyact.component import (
    BuiltinComponent,
    Element,
    Root,
)
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Gtk3Root(Root):
    def __init__(self, root: Gtk.Container):
        self.root = root
        self.tree = None

    def render(self, element: Element):
        element.component.mount(element, self.root.add, self.root.remove)
        self.root.show_all()
        Gtk.main()


class GtkBuiltinComponent(BuiltinComponent):
    pass


def create_root(root):
    return Gtk3Root(root)
