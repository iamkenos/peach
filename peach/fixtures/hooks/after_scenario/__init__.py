from typing import Any, Callable

from behave.model import Scenario, Status

from .. import Hook


class AfterScenario(Hook):
    def __init__(self, scenario: Scenario):
        super().__init__()
        self.scenario = scenario

    def on_pass(self, callback: Callable[[], Any]):
        if self.scenario.status == Status.passed:
            callback()

    def on_fail(self, callback: Callable[[], Any]):
        if self.scenario.status == Status.failed:
            callback()

    def on_error(self, callback: Callable[[], Any]):
        if self.scenario.status == Status.error:
            callback()

    def __delete_browser_recording_on_pass(self):
        def callback():
            f = self._ctx.browser.get_video_attachment_file()
            self._ctx.files.try_remove(f)

        self.on_pass(callback)

    def __delete_log_file_if_empty(self):
        f = self._ctx.files.output.scenario_log_filepath
        self._ctx.files.try_remove_if_empty(f)

    def run(self):
        self._ctx.browser.close()
        self.__delete_browser_recording_on_pass()
        self.__delete_log_file_if_empty()
