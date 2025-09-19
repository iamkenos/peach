from collections.abc import Callable
from pathlib import Path
from typing import Any

from peach.plugins.context.types import Context


def attach_evidence(self: Context, name: str, callback: Callable[[str], Any]) -> str:
    full_path = ""
    if self.is_using_behavex:
        full_path = str(Path(self.evidence_path, name).absolute())
        callback(full_path)

    return full_path
