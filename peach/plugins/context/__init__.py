from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from behave.runner import Context as BaseContext

from peach.fixtures import Fixture
from peach.fixtures.attributes.browser import Browser
from peach.fixtures.attributes.env import Env
from peach.fixtures.attributes.hooks import Hooks
from peach.plugins.context.commands import patch as patch_context_commands
from peach.plugins.context.types import Attr
from peach.plugins.locator.commands import patch as patch_locator_commands
from peach.plugins.page.commands import patch as patch_page_commands


class Context(BaseContext):
    """
    The `behave` context extended with custom props and methods.

    This is mainly used for type completion so properly define typings, args, and return types of all custom props and methods here.
    """

    # ==================================
    #   behavex
    # ==================================
    root_dir: str
    """ The resolved project root directory. Derived from the parent of where `environment.py` is. """

    output_dir: str

    outputs_dir: str

    evidence_path: str
    """ The unique `behavex` path for each scenario where evidences are stored. """

    worker_id: str
    """ A unique id tied to each behave worker. Only available when the runner used is `behavex`. """

    is_using_behavex: bool
    # worker_id is set by behavex and does not exist when the runner used is behave
    """ Whether the runner used was `behavex`. Because tests can also be launched with `behave`. """

    def scenario_log_dir(self) -> str: ...

    def scenario_log_file(self) -> str: ...

    # ==================================
    #   attributes
    # ==================================
    env: Env
    """ Interface for env variables. """

    browser: Browser
    """ Interface for the playwright fixtures. """

    hooks: Hooks
    """ Collection of functions to be called on `environment.py` hooks. """

    parameters: SimpleNamespace
    """ A simple namespace to store parameters that can be shared across steps within the same scenario."""

    # ==================================
    #   reporting
    # ==================================
    def attach_evidence(self, name: str, callback: Callable[[str], Any]) -> str: ...


def extend(ctx: Context) -> None:
    """
    Extends the `behave` context object with custom attributes and functions.

    Designed to be called immediately on the `environment.py`'s `before_all` hook.
    """
    # patch plug-ins and fixture
    patch_context_commands(ctx)
    patch_page_commands(ctx)
    patch_locator_commands(ctx)
    setattr(Fixture, Attr._ctx, ctx)

    ctx.root_dir = str(Path(ctx.config.base_dir).parent.absolute())
    ctx.output_dir = str(Path(ctx.root_dir, "output").absolute())
    ctx.outputs_dir = str(Path(ctx.output_dir, "outputs").absolute())
    ctx.worker_id = ctx.config.userdata.get("worker_id", "")
    ctx.is_using_behavex = bool(ctx.worker_id)

    # init complex attributes
    ctx.env = Env()
    ctx.browser = Browser()
    ctx.hooks = Hooks()
    ctx.parameters = SimpleNamespace()
