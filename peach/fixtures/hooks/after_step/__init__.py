from typing import Any, Callable

from behave.model import Status, Step

from .. import Hook


class AfterStep(Hook):
    def __init__(self, step: Step):
        super().__init__()
        self.step = step

    def on_pass(self, callback: Callable[[], Any]):
        if self.step.status == Status.passed:
            callback()

    def on_fail(self, callback: Callable[[], Any]):
        if self.step.status == Status.failed:
            callback()

    def on_error(self, callback: Callable[[], Any]):
        if self.step.status == Status.error:
            callback()

    def run(self):
        pass
