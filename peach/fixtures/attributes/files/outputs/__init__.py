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

        self.output_dir = self.to_absolute_path(self.root_dir, self._ctx._config.junit_directory)
        """The `behave` output directory, either coming from default or passed from the config file."""

        self.outputs_dir = self.to_absolute_path(self.output_dir, "outputs")
        """The `behavex` report directory, typically used by the default `behavex` HTML formatter."""

        self.report_dir = self.to_absolute_path(self.output_dir, "report")
        self.report_environment_filepath = self.to_absolute_path(self.report_dir, "environment.properties")

        self.__scenario_evidence_dir = None

    @property
    def scenario_evidence_dir(self):
        """The unique path for each scenario where evidences are stored."""

        if self.__scenario_evidence_dir:
            return self.__scenario_evidence_dir

        if self._ctx.is_using_behavex:
            scenario_evidence_dir = self.to_absolute_path(self._ctx.evidence_path)
        else:
            # support for the `behave` runner.
            scenario_evidence_dir = self.to_absolute_path(self.report_dir, self._ctx.scenario.identifier_hash, "evidence")

        self.__scenario_evidence_dir = scenario_evidence_dir
        return scenario_evidence_dir

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
