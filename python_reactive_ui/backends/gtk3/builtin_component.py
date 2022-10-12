from typing import Callable, Optional
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

    def _prop_has_new_value(self, new_props: Props, prop_name: str):
        return prop_name in new_props and (
            prop_name not in self._props
            or self._props[prop_name] != new_props[prop_name]
        )

    def _prop_removed(self, new_props: Props, prop_name: str):
        return prop_name not in new_props and prop_name in self._props

    def _update_prop_with_default(
        self,
        new_props: Props,
        prop_name: str,
        default,
        updater,
        prop_mapper: Callable = lambda x: x,
    ):
        if self._prop_has_new_value(new_props, prop_name):
            updater(prop_mapper(new_props[prop_name]))
        elif self._prop_removed(new_props, prop_name):
            updater(prop_mapper(default))

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

        # Simple props
        self._update_prop_with_default(
            new_props, "hexpand", False, self.gtk_widget.set_hexpand
        )
        self._update_prop_with_default(
            new_props, "vexpand", False, self.gtk_widget.set_vexpand
        )
        self._update_prop_with_default(
            new_props, "sensitive", True, self.gtk_widget.set_sensitive
        )
        self._update_prop_with_default(
            new_props, "opacity", 1.0, self.gtk_widget.set_opacity
        )
        self._update_prop_with_default(
            new_props,
            "halign",
            "fill",
            self.gtk_widget.set_halign,
            self._get_align_enum,
        )
        self._update_prop_with_default(
            new_props,
            "valign",
            "fill",
            self.gtk_widget.set_valign,
            self._get_align_enum,
        )
        self._update_prop_with_default(
            new_props, "tooltip_text", None, self.gtk_widget.set_tooltip_text
        )
        self._update_prop_with_default(
            new_props,
            "size_request",
            (-1, -1),
            lambda sr: self.gtk_widget.set_size_request(*sr),
        )
        if isinstance(self.gtk_widget, Gtk.Orientable):
            self._receive_orientable_props(new_props)

    def _receive_orientable_props(self, new_props):
        self._update_prop_with_default(
            new_props,
            "orientation",
            "horizontal",
            self.gtk_widget.set_orientation,
            self._get_orientation_enum,
        )

    def _get_orientation_enum(self, orientation: str):
        match orientation:
            case "horizontal":
                return Gtk.Orientation.HORIZONTAL
            case "vertical":
                return Gtk.Orientation.VERTICAL
            case other:
                raise ValueError(f"orientation value of {other} is not supported")

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
