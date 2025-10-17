from behave.model import Step

from .. import Hook


class BeforeStep(Hook):
    def __init__(self, step: Step):
        super().__init__()
        self.step = step

    def run(self):
        pass
