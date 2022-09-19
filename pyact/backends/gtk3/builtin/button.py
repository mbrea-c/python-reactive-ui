from gi.repository import Gtk
from dataclasses import dataclass
import logging
from typing import Callable, Optional, Tuple
from pyact.backends.gtk3.render import GtkBuiltinComponent
from pyact.component import Element, Props
import gi

gi.require_version("Gtk", "3.0")


@dataclass
class ButtonProps(Props):
    on_click: Optional[Callable] = None
    on_signal: Optional[Tuple[str, Callable]] = None


class Button(GtkBuiltinComponent):
    def _mount(self, element: Element):
        self.gtk_button = Gtk.Button.new()
        self.signal_handlers = dict()
        self.child = None
        assert isinstance(element.props, ButtonProps)
        self.receive_props(element, element.props)
        self.mounter(self.gtk_button)

    def _receive_props(self, element: Element, new_props: ButtonProps):
        logging.info(f"{self}")
        self._update_on_click(element, new_props)
        match new_props.children:
            case []:
                pass
                self.gtk_button.add(None)
            case [child]:
                old = self.child
                element.component._compare_child(
                    old, child, self.gtk_button.add, self.gtk_button.remove
                )
                self.child = child
            case _:
                raise Exception("button only supports a single child")

    def _update_on_click(self, element: Element, new_props: ButtonProps):
        if "clicked" in self.signal_handlers:
            self.gtk_button.disconnect(self.signal_handlers["clicked"])
            self.signal_handlers.pop("clicked")
        if new_props.on_click:
            self.signal_handlers["clicked"] = self.gtk_button.connect(
                "clicked", new_props.on_click
            )

    def _dismount(self, element):
        self.dismounter(self.gtk_button)
