from typing import Optional
from python_reactive_ui import Props
from python_reactive_ui.lib.core import BuiltinComponent, Children

# fmt: off
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# fmt: on


class Gtk3BuiltinComponent(BuiltinComponent):
    def _set_widget(self, gtk_widget: Gtk.Widget):
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
        if "hexpand" in new_props:
            if (
                "hexpand" not in self._props
                or self._props["hexpand"] != new_props["hexpand"]
            ):
                self.gtk_widget.set_hexpand(new_props["hexpand"])
        if "vexpand" in new_props:
            if (
                "vexpand" not in self._props
                or self._props["vexpand"] != new_props["vexpand"]
            ):
                self.gtk_widget.set_vexpand(new_props["vexpand"])
        if "halign" in new_props:
            if (
                "halign" not in self._props
                or self._props["halign"] != new_props["halign"]
            ):
                self.gtk_widget.set_halign(self._get_align_enum(new_props["halign"]))
        if "valign" in new_props:
            if (
                "valign" not in self._props
                or self._props["valign"] != new_props["valign"]
            ):
                self.gtk_widget.set_valign(self._get_align_enum(new_props["valign"]))

    def _get_align_enum(self, value):
        match value:
            case "fill":
                return Gtk.Align.FILL
            case "start":
                return Gtk.Align.START
            case "end":
                return Gtk.Align.END
            case "center":
                return Gtk.Align.CENTER
            case "baseline":
                return Gtk.Align.BASELINE
            case other:
                raise ValueError(f"Align value {other} not recognized.")
