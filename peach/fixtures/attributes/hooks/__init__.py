from typing import Callable

from behave.model import Scenario, Status, Step

from peach.fixtures import Fixture
from peach.utilities.object import inspect_obj


class Hooks(Fixture):
    def __init__(self):
        super().__init__()

    def before_all(self):
        self._ctx.browser.start()

    def after_all(self):
        self._ctx.env.export_resolved_as_file(self._ctx.files.output.report_environment_filepath)
        self._ctx.browser.stop()

    # ==================================================
    #   scenario
    # ==================================================
    def set_scenario_identifier_hash(self, scenario):
        if not self._ctx.is_using_behavex:
            inspect_obj.maybe_set_attribute(scenario, "identifier_hash", self._ctx.files.generate_uuid())

    def close_browser_page(self):
        self._ctx.browser.close()

    def delete_scenario_browser_recording_on_sucess(self, scenario):
        def callback():
            f = self._ctx.browser.get_video_attachment_file()
            self._ctx.files.try_remove(f)

        self.on_scenario_success(scenario, callback)

    def delete_scenario_log_file_if_empty(self):
        f = self._ctx.files.output.scenario_log_filepath
        self._ctx.files.try_remove_if_empty(f)

    def on_scenario_success(self, scenario: Step, callback: Callable[[], None]):
        if scenario.status == Status.passed:
            callback()

    def on_scenario_error(self, scenario: Step, callback: Callable[[], None]):
        if scenario.status == Status.error:
            callback()

    def suffix_scenario_name_with_example_id(self, scenario: Scenario):
        """Suffixes the scenario name with the value of the first column of the example table."""
        if scenario._row is not None:
            id, *_ = list(scenario._row)
            scenario.name = f"{scenario.name}: {id}"

    def assign_pending_step_exception_if_any(self, scenario: Scenario):
        steps = filter(lambda step: step.status == Status.undefined, scenario.steps)
        for step in steps:
            step: Step
            if step.exception is None:
                step.store_exception_context(Exception(f"Pending step implementation: '{step.keyword} {step.name}'."))

    def post_process_scenario_errors(self, scenario: Scenario):
        self.assign_pending_step_exception_if_any(scenario)

    # ==================================================
    #   step
    # ==================================================
    def attach_evidences_on_error(self, step: Step):
        def callback():
            pass  # create attachments under `self._ctx.files.output.scenario_evidence_dir` as needed

        self.on_step_error(step, callback)

    def on_step_error(self, step: Step, callback: Callable[[], None]):
        if step.status in [Status.failed, Status.error] and step.exception:
            callback()
