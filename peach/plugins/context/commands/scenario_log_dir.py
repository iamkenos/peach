from pathlib import Path

from peach.plugins.context.types import Context


def scenario_log_dir(self: Context) -> str:
    return str(Path(Path(self.evidence_path).parent).absolute())
