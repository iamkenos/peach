from pathlib import Path

from peach.plugins.context.types import Context
from peach.plugins.plugin import patch as do_patch


def patch(ctx: Context) -> None:
    """Patch context with exposed functions under bindings."""
    package = "peach.plugins.context.commands"
    package_path = str(Path(__file__).parent)

    do_patch(
        commands_package=package,
        commands_package_path=package_path,
        class_or_instance_to_patch=ctx,
    )
