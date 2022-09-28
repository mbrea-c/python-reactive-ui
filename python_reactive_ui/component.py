from enum import Enum, auto
import logging
from typing import Callable, Dict, List, Optional, Tuple
from itertools import zip_longest
import inspect


class Root:
    def render(self, component: "Component"):
        raise NotImplementedError()


Props = Dict
Children = List["Component"]


class ActionType(Enum):
    SWAP = auto()
    MOUNT = auto()
    DISMOUNT = auto()
    UPDATE = auto()
    ADD_CHILD = auto()
    REMOVE_CHILD = auto()


Action = Tuple[ActionType, Tuple]
Actions = List[Action]


class Component:
    def __init__(self):
        self._children: Children = []
        self._props: Props = dict()
        self._render_result: Optional["Component"] = None
        self._render_parent: Optional["Component"] = None

        # State
        self._state: Dict = dict()
        self._state_counter = 0

        # Other
        self._print_on_render = False
        self._is_mounted = False

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"<{type(self).__name__}>"

    def render(self) -> "Component":
        if self._print_on_render:
            print_tree(self)
        self._state_counter = 0
        result = self._render(self._props, self._children)
        result._render_parent = self
        return result

    def _render(self, props: Props, children: Children) -> "Component":
        raise NotImplementedError()

    def _render_close(self):
        if not isinstance(self, BuiltinComponent):
            self._render_result = self.render()
            self._render_result._render_close()

    def trigger_rerender(
        self, mounter=Optional[Callable], dismounter=Optional[Callable]
    ):
        mounter = mounter if (mounter is not None) else self._mounter
        dismounter = dismounter if (dismounter is not None) else self._dismounter

        if not isinstance(self, BuiltinComponent):
            new_element = self.render()
            actions = self._compare(self._render_result, new_element)
            self._perform_actions(actions, mounter, dismounter)  # type: ignore

    def _compare_children(
        self,
        old_children: List["Component"],
        new_children: List["Component"],
    ) -> Actions:
        actions = []
        for i, (old, new) in enumerate(zip_longest(old_children, new_children)):
            curr_actions = self._compare(old, new)
            if len(curr_actions) == 1:
                [action] = curr_actions
                match action:
                    case (ActionType.MOUNT, (new,)):
                        actions.extend([action, (ActionType.ADD_CHILD, (new,))])
                    case (ActionType.DISMOUNT, (old,)):
                        actions.extend([action, (ActionType.REMOVE_CHILD, (old,))])
                    case (ActionType.SWAP, (old, new)):
                        actions.extend([action, (ActionType.ADD_CHILD, (old, i))])
                    case other:
                        actions.append(other)
        return actions

    def _compare(
        self,
        old: Optional["Component"],
        new: Optional["Component"],
    ) -> Actions:
        if new is not None:
            if old is None:
                return [(ActionType.MOUNT, (new,))]

            elif not type(old) == type(new):
                return [(ActionType.SWAP, (old, new))]
            else:
                if old._props != new._props:
                    return [(ActionType.UPDATE, (old, new))]
                if len(self._compare_children(old._children, new._children)) > 0:
                    return [(ActionType.UPDATE, (old, new))]
        else:
            if old is not None:
                return [(ActionType.DISMOUNT, (old,))]
        return []

    def _perform_actions(
        self, actions: Actions, mounter: Callable, dismounter: Callable
    ):
        for action in actions:
            match action:
                case (ActionType.MOUNT, (new,)):
                    if new._is_mounted:
                        new.dismount()
                    new.mount(mounter, dismounter)
                case (ActionType.DISMOUNT, (old,)):
                    old.dismount()
                case (ActionType.SWAP, (old, new)):
                    if old._render_parent is not None:
                        assert old._render_parent._render_child is old
                        assert new._render_parent is not None
                        assert new._render_parent is old._render_parent
                        old._render_parent._render_child = new
                    old.dismount()
                    new.mount(mounter, dismounter)
                case (ActionType.UPDATE, (old, new)):
                    old.receive_props(new._props)
                    old.receive_children(new._children)
                    old.trigger_rerender()
                case (ActionType.ADD_CHILD, (new,)):
                    self._add_child(new)
                case (ActionType.ADD_CHILD, (new, i)):
                    self._add_child(new, i)
                case (ActionType.REMOVE_CHILD, (old,)):
                    self._remove_child(old)

    def receive_props(self, new_props: Props):
        self._receive_props(new_props)

    def _receive_props(self, new_props: Props):
        self._props = new_props

    def receive_children(self, new_children: Children):
        self._receive_children(new_children)

    def _receive_children(self, new_children: Children):
        self._children = new_children

    def mount(
        self,
        mounter: Optional[Callable] = None,
        dismounter: Optional[Callable] = None,
    ):
        if mounter is not None:
            self._mounter = mounter
        if dismounter is not None:
            self._dismounter = dismounter
        assert mounter is not None
        assert dismounter is not None
        assert not self._is_mounted
        self._is_mounted = True
        self._mount()

    def _mount(self):
        assert self._render_result is not None
        return self._render_result.mount(self._mounter, self._dismounter)

    def dismount(self):
        assert self._is_mounted
        assert self._dismounter is not None
        self._is_mounted = False
        self._dismount()

    def _dismount(self):
        assert self._render_result is not None
        return self._render_result.dismount()

    def _add_child(self, child: "Component", index: Optional[int] = None):
        if index is not None and len(self._children) > index:
            self._children[index] = child
        else:
            self._children.append(child)

    def _remove_child(self, child: "Component"):
        self._children.remove(child)


class BuiltinComponent(Component):
    def _mount(self):
        raise NotImplementedError()

    def _receive_props(self, new_props: Props):
        raise NotImplementedError()

    def _receive_children(self, new_children: Children):
        raise NotImplementedError()

    def _dismount(self):
        raise NotImplementedError()


def create_element(
    component,
    props: Props,
    children: Optional[Children] = None,
) -> Component:
    if not (inspect.isclass(component) and issubclass(component, Component)):
        raise ValueError("`component` argument should be a subclass of `Component`")

    instance = component()

    _children: Children = [] if children is None else children
    instance.receive_props(props)
    instance.receive_children(_children)
    instance._render_close()
    return instance


def use_state(component: Component, initial_value=None):
    counter = component._state_counter

    def set_func(new_value):
        component._state[counter] = new_value
        component.trigger_rerender()

    if component._state_counter not in component._state:
        component._state[component._state_counter] = initial_value
    elem = component._state[component._state_counter]
    component._state_counter += 1
    return elem, set_func


def _print_actions(actions):
    ss = "[\n"
    for action in actions:
        (action_type, stuff) = action
        s = f"({str(action_type)}"
        for a in stuff:
            s += f", {a}"
        s += ")"
        ss += f"\t{s}\n"
    ss += "]"
    return ss


def print_tree(component: Component, depth=0):
    print("| " * depth + f"{component}")
    if not isinstance(component, BuiltinComponent):
        print("| " * depth + "|" + f"Renders:")
        if component._render_result:
            print_tree(component._render_result, depth=depth + 1)
    if len(component._children) > 0:
        print("| " * depth + "|" + f"Children:")
        for child in component._children:
            print_tree(child, depth=depth + 1)
