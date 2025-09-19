import os
from pathlib import Path
from typing import Callable

from behave.model import Scenario, Status, Step

from peach.fixtures import Fixture


class Hooks(Fixture):
    def __init__(self):
        super().__init__()

    def before_all(self):
        self._ctx.browser.start()

    def after_all(self):
        environment_properties_filepath = str(Path(self._ctx.output_dir, "allure", "environment.properties").absolute())

        self._ctx.env.export_resolved_as_file(environment_properties_filepath)
        self._ctx.browser.stop()

    # ==================================================
    #   scenario
    # ==================================================
    def delete_scenario_log_file_if_empty(self):
        f = self._ctx.scenario_log_file()
        if os.path.exists(f) and os.path.getsize(f) == 0:
            try:
                os.remove(f)
            except Exception as e:
                str(e)
                pass

    def on_scenario_error(self, scenario: Step, callback: Callable[[], None]):
        if scenario.status == Status.error:
            callback()

    def prefix_scenario_name_with_example_id(self, scenario: Scenario):
        """Prefixes the scenario name with the value of the first column of the example table."""
        if scenario._row is not None:
            id, *_ = list(scenario._row)
            scenario.name = f"{id}: {scenario.name}"

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
            self._ctx.browser.attach_screenshot()

        self.on_step_error(step, callback)

    def on_step_error(self, step: Step, callback: Callable[[], None]):
        if step.status in [Status.failed, Status.error] and step.exception:
            callback()
