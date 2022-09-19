from gi.repository import Gtk
from dataclasses import dataclass
from pyact.backends.gtk3.render import GtkBuiltinComponent
from pyact.component import Element, Props
import gi

gi.require_version("Gtk", "3.0")


@dataclass
class BoxProps(Props):
    orientation: str = "horizontal"
    spacing: int = 0


class Box(GtkBuiltinComponent):
    def _mount(self, element: Element):
        self.gtk_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        assert isinstance(element.props, BoxProps)
        self._receive_props(element, element.props, True)
        self.mounter(self.gtk_box)

    def _receive_props(self, element: Element, new_props: BoxProps, init: bool = False):
        if init:
            self._init_children(element, self.gtk_box.add, self.gtk_box.remove)
        else:
            self._update_children(
                element, new_props.children, self.gtk_box.add, self.gtk_box.remove
            )
        self._update_orientation(element, new_props.orientation)
        self.gtk_box.set_spacing(new_props.spacing)

    def _update_orientation(self, element: Element, orientation: str):
        match orientation:
            case "horizontal":
                self.gtk_box.set_orientation(Gtk.Orientation.HORIZONTAL)
            case "vertical":
                self.gtk_box.set_orientation(Gtk.Orientation.VERTICAL)
            case other:
                raise ValueError(f"orientation value of {other} is not supported")

    def _dismount(self, element):
        self.dismounter(self.gtk_box)
