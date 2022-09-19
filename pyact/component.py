import logging
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass, field
from itertools import zip_longest
import inspect


@dataclass
class Props:
    children: List["Element"] = field(default_factory=list)

    def __repr__(self):
        return f"children={self.children}"


class Element:
    def __init__(self, component: "Component", props: Props):
        self.component: "Component" = component
        self.props: Props = props
        self.state: Dict = dict()
        self.state_counter = 0
        self.render_result: Optional[Element] = None

    def __eq__(self, other: "Element"):
        return (
            self.component == other.component
            and self.props == other.props
            and self.state == other.state
            and self.render_result == other.render_result
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"<{type(self.component).__name__}>"


class Root:
    def render(self, element: Element):
        raise NotImplementedError()


FunctionalComponent = Callable[[Element, Props], Element]

# Steps in lifecycle:
# 1. Render component tree
# 2. Determine diff actions
# 3. Execute dismounts
# 4. Exectue mounts
# 5. Execute receive_props


class Component:
    def __init__(self):
        pass

    def __eq__(self, other):
        return type(self) == type(other)

    def render(self, element: Element, props: Props) -> Element:
        raise NotImplementedError()

    def trigger_rerender(
        self, element, mounter=Optional[Callable], dismounter=Optional[Callable]
    ):
        mounter = mounter if (mounter is not None) else self.mounter
        dismounter = dismounter if (dismounter is not None) else self.dismounter

        if not isinstance(element.component, BuiltinComponent):
            new_element = self.render(element, element.props)
            self._compare_child(
                element.render_result, new_element, mounter, dismounter, parent=element
            )  # type: ignore

    def _update_children(
        self,
        element: Element,
        new_children: List[Element],
        mounter: Callable,
        dismounter: Callable,
    ):
        for old, new in zip_longest(
            element.props.children,
            new_children,
        ):
            self._compare_child(old, new, mounter, dismounter)

    def _init_children(self, element: Element, mounter: Callable, dismounter: Callable):
        for child in element.props.children:
            child.component.mount(child, mounter, dismounter)

    def _compare_child(
        self,
        old_element: Optional[Element],
        new_element: Optional[Element],
        mounter: Callable,
        dismounter: Callable,
        parent: Optional[Element] = None,
    ):
        if new_element is not None:
            if old_element is None or not type(old_element.component) == type(
                new_element.component
            ):
                logging.info(f"Replacing {old_element} with {new_element}")
                if old_element:
                    old_element.component.dismount(old_element)
                if parent:
                    parent.render_result = new_element
                new_element.component.mount(new_element, mounter, dismounter)
            elif old_element.props != new_element.props:
                logging.info(f"Sending props to {old_element}")
                old_element.component.receive_props(old_element, new_element.props)
                old_element.component.trigger_rerender(old_element)
            else:
                logging.info(f"Re-rendering {old_element}")
                old_element.component.trigger_rerender(old_element)
        else:
            if old_element is not None:
                old_element.component.dismount(old_element)

    def mount(
        self,
        element: Element,
        mounter: Optional[Callable] = None,
        dismounter: Optional[Callable] = None,
    ):
        if mounter is not None:
            self.mounter = mounter
        if dismounter is not None:
            self.dismounter = dismounter
        assert mounter is not None and dismounter is not None
        logging.info(f"Mounting {element}")
        self._mount(element)

    def _mount(self, element):
        assert element.render_result is not None
        return element.render_result.component.mount(
            element.render_result, self.mounter, self.dismounter
        )

    def receive_props(self, element: Element, new_props: Props):
        self._receive_props(element, new_props)

    def _receive_props(self, element: Element, new_props: Props):
        element.props = new_props

    def dismount(self, element: Element):
        assert self.dismounter is not None
        logging.info(f"Dismounting {element}")
        self._dismount(element)

    def _dismount(self, element: Element):
        assert element.render_result is not None
        return element.render_result.component.dismount(element.render_result)


class _BaseComponent(Component):
    def __init__(self, fc: FunctionalComponent):
        self.fc = fc

    def render(self, element: Element, props: Props) -> Element:
        element.state_counter = 0
        return self.fc(element, props)

    def __eq__(self, other):
        return self.fc == other.fc


class BuiltinComponent(Component):
    def _mount(self, element: Element):
        raise NotImplementedError()

    def _receive_props(self, element: Element, new_props: Props):
        raise NotImplementedError()

    def _dismount(self, element: Element):
        raise NotImplementedError()


def createElement(component, props, children: Optional[List[Element]] = None):
    children = children if (children is not None) else []
    props.children = children

    if inspect.isclass(component):
        component = component()
    else:
        component = _BaseComponent(component)

    element = Element(component, props)
    repopulate_elem_tree(element)
    return element


def use_state(element: Element, initial_value=None):
    counter = element.state_counter

    def set_func(new_value):
        element.state[counter] = new_value
        element.component.trigger_rerender(element)

    if element.state_counter not in element.state:
        element.state[element.state_counter] = initial_value
    elem = element.state[element.state_counter]
    element.state_counter += 1
    return elem, set_func


def repopulate_elem_tree(element: Element):
    if not isinstance(element.component, BuiltinComponent):
        element.render_result = element.component.render(element, element.props)
        repopulate_elem_tree(element.render_result)


def print_tree(element: Element, depth=0):
    print(" " * depth + f"{element}")
    for child in element.props.children:
        print_tree(child, depth=depth + 1)
    if element.render_result:
        print_tree(element.render_result, depth=depth + 1)
