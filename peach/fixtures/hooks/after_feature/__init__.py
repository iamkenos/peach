from typing import Any, Callable

from behave.model import Feature, Status

from .. import Hook


class AfterFeature(Hook):
    def __init__(self, feature: Feature):
        super().__init__()
        self.feature = feature

    def on_pass(self, callback: Callable[[], Any]):
        if self.feature.status == Status.passed:
            callback()

    def on_fail(self, callback: Callable[[], Any]):
        if self.feature.status == Status.failed:
            callback()

    def on_error(self, callback: Callable[[], Any]):
        if self.feature.status == Status.error:
            callback()

    def run(self):
        pass
