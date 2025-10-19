import os
import uuid
from pathlib import Path

import numpy as np
import pandas as pd

from peach.fixtures import Fixture
from peach.fixtures.assertions import Assertions
from peach.utilities.string import format_str


class IOFiles(Fixture):
    def __init__(self):
        super().__init__()
        self.root_dir = self.to_absolute_path(Path(self._ctx.config.base_dir).parent)
        """ The resolved project root directory. Derived from the parent of where `environment.py` is. """

    def stitch_path(self, *args) -> Path:
        return Path(*args)

    def to_absolute_path(self, *args) -> str:
        return str(self.stitch_path(*args).absolute())

    def generate_uuid(self):
        return uuid.uuid4().hex

    def mkdirp(self, filepath: str):
        directory = os.path.dirname(filepath)
        os.makedirs(directory, exist_ok=True)

    def write(self, filepath: str, content: str):
        with open(filepath, "w") as f:
            f.write(content)

    def read_csv_as_df(self, filepath: str, *, replace_nan_with="", transform_headers=True):
        """
        Actually returns a partially packed tuple of `DataFrame` and `str` where the first item is the csv as df and the second is the filepath.

        The result is always the first item unless otherwise unpacked.
        """
        expect = Assertions()
        expect.set_exception_type(FileNotFoundError).file_exists(filepath).evaluate()

        df = pd.read_csv(filepath)
        df = df.replace({np.nan: replace_nan_with})
        df.source_file = filepath
        if transform_headers:
            df.columns = [format_str.to_snake(col) for col in df.columns]

        return df

    def try_remove(self, filepath: str):
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

    def try_remove_if_empty(self, filepath: str):
        if os.path.getsize(filepath) == 0:
            self.try_remove(filepath)
