import importlib
import inspect
import pkgutil
from pathlib import Path


def bind(ctx):
    """Patch context with exposed functions under bindings."""
    bindings = "bindings"
    package = "fixtures.context.bindings"
    package_path = str(Path(__file__).parent.parent / bindings)

    for _, modname, _ in pkgutil.iter_modules([package_path]):
        module = importlib.import_module(f"{package}.{modname}")

        for name, fn in inspect.getmembers(module, inspect.isfunction):
            # bind only functions that expect a Context as first arg
            if fn.__code__.co_varnames[:1] == ("self",):
                setattr(ctx, name, fn.__get__(ctx))
