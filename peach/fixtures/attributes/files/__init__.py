from .io_files import IOFiles  # noqa

from .inputs import InputFiles
from .outputs import OutputFiles


class Files(IOFiles):
    def __init__(self):
        super().__init__()

        self.input = InputFiles()
        self.output = OutputFiles()
