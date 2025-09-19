import inspect


def get_own_attributes(prototype) -> list[str]:
    all_attributes = prototype.__dict__.keys()  # use in favor of dir() so it's not alphabetized by default
    own_attributes = []

    for attr in all_attributes:
        attr_value = getattr(prototype, attr)
        if not inspect.isfunction(attr_value) and not inspect.ismethod(attr_value) and not inspect.isbuiltin(attr_value):
            own_attributes.append(attr)

    return own_attributes
