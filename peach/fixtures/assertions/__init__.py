from .dataframe_assertions import DataFrameAssertions
from .file_assertions import FileAssertions


class Assertions(DataFrameAssertions, FileAssertions):
    pass
