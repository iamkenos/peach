from .. import Hook


class AfterAll(Hook):
    def __init__(self):
        super().__init__()

    def run(self):
        self._ctx.env.export_resolved_as_file(self._ctx.files.output.report_environment_filepath)
        self._ctx.browser.stop()
