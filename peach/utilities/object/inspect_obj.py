import inspect
from typing import Any


def get_own_attributes(instance) -> list[str]:
    all_attributes = instance.__dict__.keys()  # use in favor of dir() so it's not alphabetized by default
    own_attributes = []

    for attr in all_attributes:
        attr_value = getattr(instance, attr)
        if not inspect.isfunction(attr_value) and not inspect.ismethod(attr_value) and not inspect.isbuiltin(attr_value):
            own_attributes.append(attr)

    return own_attributes


def maybe_set_attribute(instance, name, value) -> Any:
    if not hasattr(instance, name):
        setattr(instance, name, value)
    return getattr(instance, name)
