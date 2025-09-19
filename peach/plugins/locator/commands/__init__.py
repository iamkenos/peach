from pathlib import Path

from playwright.sync_api._generated import Locator

from peach.plugins.context.types import Context
from peach.plugins.plugin import patch as do_patch


def patch(ctx: Context):
    """Patch locator with custom commands."""
    package = "peach.plugins.locator.commands"
    package_path = str(Path(__file__).parent)

    do_patch(
        commands_package=package,
        commands_package_path=package_path,
        class_or_instance_to_patch=Locator,
    )
