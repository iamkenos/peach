import inspect
from pathlib import Path
from types import SimpleNamespace

from behave.runner import Context as BaseContext

from .attributes import init
from .attributes.browser import Browser
from .attributes.env import Env
from .attributes.hooks import Hooks
from .bindings import bind
from .bindings.attach_evidence import AttachEvidenceFn


class Context(BaseContext):
    """
    The `behave` context extended with custom props and methods.

    This is mainly used for type completion so properly define typings, args, and return types of all custom props and methods here.
    """

    # ==================================
    #   behavex
    # ==================================
    root_dir: str = None
    """ The resolved project root directory. Derived from the parent of where `environment.py` is. """

    output_dir: str = None

    evidence_path: str = None
    """ The unique `behavex` path for each scenario where evidences are stored. """

    worker_id: str = None
    """ A unique id tied to each behave worker. Only available when the runner used is `behavex`. """

    is_using_behavex: bool = None
    # worker_id is set by behavex and does not exist when the runner used is behave
    """ Whether the runner used was `behavex`. Because tests can also be launched with `behave`. """

    # ==================================
    #   attributes
    # ==================================
    env: Env = None
    """ Interface for env variables. """

    browser: Browser = None
    """ Interface for the playwright fixtures. """

    hooks: Hooks = None
    """ Collection of functions to be called on `environment.py` hooks. """

    parameters: SimpleNamespace = None
    """ A simple namespace to store parameters that can be shared across steps within the same scenario."""

    # ==================================
    #   reporting
    # ==================================
    def attach_evidence(self, name: str, callback: AttachEvidenceFn) -> None: ...


def extend(ctx: Context) -> None:
    """
    Extends the `behave` context object with custom attributes and functions.

    Designed to be called immediately on the `environment.py`'s `before_all` hook.
    """
    init(ctx, Context)
    bind(ctx)

    ctx.root_dir = str(Path(ctx.config.base_dir).parent.absolute())
    ctx.output_dir = str(Path(ctx.config.junit_directory).absolute())
    ctx.worker_id = ctx.config.userdata.get("worker_id", "")
    ctx.is_using_behavex = bool(ctx.worker_id)

    ctx.env = Env(ctx)
    ctx.browser = Browser(ctx)
    ctx.hooks = Hooks(ctx)
    ctx.parameters = SimpleNamespace()


def resolve_behave_context() -> Context:
    """
    Attempts to return the `behave` context object via reflection.
    Only use this for edge cases as walking the stack can be unperformant if called often.
    """
    context = None
    try:
        stack = inspect.stack()
        if len(stack) > 2:
            behave_frame_substrings = ["behave", "runner"]
            behave_frame = next((frame for frame in stack if all(sub in frame.filename for sub in behave_frame_substrings)), None)
            frame_locals = behave_frame.frame.f_locals if behave_frame else None
            context = frame_locals.get("ctx", frame_locals.get("context", None)) if behave_frame else None
    except Exception:
        pass
    return context
