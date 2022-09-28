from python_reactive_ui import Component


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
