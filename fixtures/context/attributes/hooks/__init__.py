from typing import Callable

from behave.model import Scenario, Status, Step

from fixtures.context.types import Context


class Hooks:
    def __init__(self, ctx: Context):
        self._ctx = ctx

    def before_all(self):
        self._ctx.browser.start()

    def after_all(self):
        self._ctx.browser.stop()

    def attach_evidences(self) -> None:
        self._ctx.browser.attach_screenshot()

    # ==================================================
    #   scenario
    # ==================================================
    def on_scenario_error(self, scenario: Step, callback: Callable[[], None]) -> None:
        if scenario.status == Status.error:
            callback()

    def prefix_scenario_name_with_example_id(self, scenario: Scenario) -> None:
        """Prefixes the scenario name with the value of the first column of the example table."""
        if scenario._row is not None:
            id, *_ = list(scenario._row)
            scenario.name = f"{id}: {scenario.name}"

    def assign_pending_step_exception_if_any(self, scenario: Scenario) -> None:
        steps = filter(lambda step: step.status == Status.undefined, scenario.steps)
        for step in steps:
            step: Step
            if step.exception is None:
                step.store_exception_context(Exception(f"Pending step implementation: '{step.keyword} {step.name}'."))

    def post_process_scenario_errors(self, scenario: Scenario) -> None:
        self.assign_pending_step_exception_if_any(scenario)

    # ==================================================
    #   step
    # ==================================================
    def on_step_error(self, step: Step, callback: Callable[[], None]) -> None:
        if step.status in [Status.failed, Status.error] and step.exception:
            callback()
