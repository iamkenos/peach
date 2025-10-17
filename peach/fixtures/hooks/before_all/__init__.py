from .. import Hook


class BeforeAll(Hook):
    def __init__(self):
        super().__init__()

    def run(self):
        self._ctx.browser.start()
