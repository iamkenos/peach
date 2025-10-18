import glob
from pathlib import Path

from ..io_files import IOFiles


class OutputFiles(IOFiles):
    """
    Interface for output files.

    **NOTE**

    Properties that reference the scenario evidence dir must be declared as a getter
    because it can only be called from a scenario context, meaning it has to be fetched
    during run-time and cannot be set upfront during construct-time.

    Doing otherwise would yield:
    `Exception: "evidence_path" is only accessible in the context of a test scenario.`
    """

    def __init__(self):
        super().__init__()

        self.output_dir = self.to_absolute_path(self.root_dir, "output")
        """The `behave` output directory."""

        self.outputs_dir = self.to_absolute_path(self.output_dir, "outputs")
        """The `behavex` report directory, typically used by the default `behavex` HTML formatter."""

        self.report_dir = self.to_absolute_path(self.output_dir, "report")
        self.report_environment_filepath = self.to_absolute_path(self.report_dir, "environment.properties")

    @property
    def scenario_evidence_dir(self):
        """The unique path for each scenario where evidences are stored."""

        if self._ctx.is_using_behavex:
            return self.to_absolute_path(self._ctx.evidence_path)
        else:
            # support for the `behave` runner.
            return self.to_absolute_path(self.report_dir, self._ctx.scenario.identifier_hash, "evidence")

    @property
    def scenario_evidence_filepaths(self):
        pattern = self.to_absolute_path(self.scenario_evidence_dir, "*.*")
        return glob.glob(pattern, recursive=True)

    @property
    def scenario_log_dir(self):
        return self.to_absolute_path(Path(self.scenario_evidence_dir).parent)

    @property
    def scenario_log_filepath(self):
        return self.to_absolute_path(self.scenario_log_dir, "scenario.log")

    def create_evidence_file(self, filename: str = "", data: str = ""):
        filepath = self.to_absolute_path(self.scenario_evidence_dir, filename)
        self.write(filepath, data)

    def try_create_evidence_file(self, filename: str = "", data: str = ""):
        try:
            self.create_evidence_file(filename, data)
        except Exception:
            pass
