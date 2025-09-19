from pathlib import Path
from typing import Protocol

from peach.fixtures.context.types import Context


class AttachEvidenceFn(Protocol):
    def __call__(self, name: str, full_path: str) -> None: ...


def attach_evidence(self: Context, name: str, callback: AttachEvidenceFn) -> None:
    full_path = ""
    if self.is_using_behavex:
        full_path = str(Path(self.evidence_path, name).absolute())
        callback(name, full_path)

    return full_path
