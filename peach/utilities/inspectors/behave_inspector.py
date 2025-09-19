import inspect
from typing import Any

from peach.plugins.context.types import Attr, Context


def resolve_context() -> Context:
    """
    Attempts to return the `behave` context object via reflection.
    Only use this for edge cases as walking the stack can be unperformant if called often.
    """
    resolved: Any = None
    try:
        stack = inspect.stack()
        if len(stack) > 2:
            behave_frame_substrings = ["behave", "runner"]
            behave_frame = next((frame for frame in stack if all(sub in frame.filename for sub in behave_frame_substrings)), None)
            f_locals = behave_frame.frame.f_locals if behave_frame else None
            resolved = f_locals.get(Attr.ctx, f_locals.get(Attr.context, f_locals.get("self", dict()).context)) if behave_frame and f_locals else None
    except Exception:
        pass
    return resolved
