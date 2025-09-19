import importlib
import inspect
import pkgutil
import types

from peach.plugins.context.types import Any


def patch(
    commands_package: str,
    commands_package_path: str,
    class_or_instance_to_patch: Any,
):
    """
    Patch a class prototype or an instance of it with custom commands. Note that this will only patch new commands and properties.
    Members already existing in `class_or_instance_to_patch` will be silently ignored.
    """

    def setter(class_or_instance_to_patch, modname, member):
        if inspect.isclass(class_or_instance_to_patch):
            setattr(class_or_instance_to_patch, modname, member)
        else:  # assume instance so bind it to the instance instead
            setattr(class_or_instance_to_patch, modname, types.MethodType(member, class_or_instance_to_patch))

    for _, modname, _ in pkgutil.iter_modules([commands_package_path]):
        module = importlib.import_module(f"{commands_package}.{modname}")
        member = getattr(module, modname)

        if inspect.isfunction(member) and member.__code__.co_varnames[:1] == ("self",):
            if not inspect.isfunction(getattr(class_or_instance_to_patch, modname, None)):
                setter(class_or_instance_to_patch, modname, member)
        elif isinstance(member, property):
            if not hasattr(class_or_instance_to_patch, modname):
                setter(class_or_instance_to_patch, modname, member)
