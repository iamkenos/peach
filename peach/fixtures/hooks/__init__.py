from peach.fixtures import Fixture


class Hook(Fixture):
    def __init__(self):
        super().__init__()

    def run(self): ...
