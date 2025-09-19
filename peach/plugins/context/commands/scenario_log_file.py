from pathlib import Path

from peach.plugins.context.types import Context


def scenario_log_file(self: Context) -> str:
    path = str(Path(self.scenario_log_dir(), "scenario.log").absolute())
    return path
