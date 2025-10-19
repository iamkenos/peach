from peach.utilities.object import inspect_obj


class EnumLike:
    pass

    @classmethod
    def get(cls, attr: str):
        try:
            return getattr(cls, attr.upper())
        except Exception:
            return attr

    @classmethod
    def get_all(cls):
        try:
            keys = inspect_obj.get_own_attributes(cls)
            return list(map(lambda key: getattr(cls, key), keys))
        except Exception:
            return []
