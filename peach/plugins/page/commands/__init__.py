from pathlib import Path

from playwright.sync_api._generated import Page

from peach.plugins.context.types import Attr, Context
from peach.plugins.plugin import patch as do_patch


def patch(ctx: Context):
    """Patch page with custom commands."""
    package = "peach.plugins.page.commands"
    package_path = str(Path(__file__).parent)

    setattr(Page, Attr._ctx, ctx)
    do_patch(
        commands_package=package,
        commands_package_path=package_path,
        class_or_instance_to_patch=Page,
    )
