from dataclasses import dataclass, field
from typing import Optional
from pyact.backends.gtk3.render import GtkBuiltinComponent
from pyact.component import Element, Props
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@dataclass
class LabelProps(Props):
    text: Optional[str] = None


class Label(GtkBuiltinComponent):
    def _mount(self, element: Element):
        self.gtk_label = Gtk.Label.new("")
        assert isinstance(element.props, LabelProps)
        self.receive_props(element, element.props)
        self.mounter(self.gtk_label)

    def _receive_props(self, element: Element, new_props: LabelProps):
        self.gtk_label.set_text(new_props.text)

    def _dismount(self, element):
        self.dismounter(self.gtk_label)
