from behave.runner import Context as BaseContext
from typing import NewType


class ContextFixture(BaseContext):
    foo: bool

    bar: list[str]


Context = NewType("Context", ContextFixture)
