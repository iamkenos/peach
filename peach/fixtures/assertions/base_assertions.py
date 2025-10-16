from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Type

from peach.utilities.object import format_obj
from peach.utilities.string import format_str

from ...fixtures import Fixture


def beautify_value(value: Any):
    return format_str.indent(f"\n{format_obj.beautify(value)}") if isinstance(value, (list, dict)) else value


def beautify_kwargs(kwargs: dict):
    args: list = []
    for key, value in kwargs.items():
        prop = format_str.to_sentence_case(key)
        value = beautify_value(value)
        args.append(f"\n{prop}: {value}")
    result = "".join(args) if args else ""
    return result


class Assertion(object):
    def __init__(self, name: str, **kwargs):
        super().__init__()
        is_not, message = "is_not", "message"
        self.message: str = kwargs.get(message, "")
        self.is_not: bool = kwargs.get(is_not, False)
        self.is_success: bool = False
        self.index: int = None
        self.name = f"expect.{name}(...)"
        self.__args: SimpleNamespace = SimpleNamespace(**{key: value for key, value in kwargs.items() if key not in [is_not, message]})

    @property
    def args(self) -> SimpleNamespace:
        return self.__args

    def check(self):
        args = self.args.__dict__
        has_expected_value = hasattr(self, "expected")
        has_actual_value = hasattr(self, "actual")
        expected_str = f"\nExpected{' (Not)' if self.is_not else ''}: {beautify_value(self.expected)}" if has_expected_value else ""
        actual_str = f"\nActual: {beautify_value(self.actual)}" if has_actual_value else ""
        message_str = f"\nMessage: {self.message}" if bool(self.message) else ""

        self.assertion_result = not self.is_success if self.is_not else self.is_success
        self.assertion_message = f"""
Assertion #{self.index + 1}: {self.name}

Result: {"Success" if self.assertion_result else "Failed"}{actual_str}{expected_str}{message_str}{beautify_kwargs(args)}
""".strip()
        self.assertion_message = format_str.indent(f"\n{self.assertion_message}")
        return self


@dataclass
class Result:
    results: list[Assertion]
    is_success: bool
    message: str


class BaseAssertions(Fixture):
    def __init__(self, **kwargs):
        self.ExceptionType = AssertionError
        self.assertions: list[Assertion] = []
        self.result: Result = None
        self.__name: str = self.__class__.__name__
        self.__soft: bool = False
        self.__args: SimpleNamespace = SimpleNamespace(**kwargs)

    @property
    def args(self) -> SimpleNamespace:
        return self.__args

    @property
    def is_soft(self) -> bool:
        return self.__soft

    def clear_assertions(self):
        self.assertions = []

    def add_assertion(self, assertion: Assertion):
        assertion.index = len(self.assertions)
        self.assertions.append(assertion)
        return self

    def set_exception_type(self, e: Type[Exception]):
        self.ExceptionType = e
        return self

    def soft(self, state=True):
        self.__soft = state
        return self

    def evaluate(self, clear_assertions=True, **kwargs: Any):
        results = []
        for assertion in self.assertions:
            assertion: Assertion
            results.append(assertion.check())

        failed_count = len(list(filter(lambda result: not result.assertion_result, results)))
        total_count = len(self.assertions)
        message = ""
        is_success = failed_count == 0

        if not is_success:
            display_name = format_str.humanize(format_str.underscore(self.__name)).lower()
            header = f"\nFailed on {failed_count}/{total_count} {display_name}.{beautify_kwargs(kwargs)}\n"
            body = "\n  --------------------------------".join(map(lambda result: result.assertion_message, results))
            message = format_str.ansi_red(f"{header}{body}")

        self.result = Result(results=results, is_success=is_success, message=message)
        try:
            should_raise = not self.result.is_success and not self.__soft
            if should_raise:
                raise self.ExceptionType(self.result.message)
            else:
                return self.result.is_success
        finally:
            if clear_assertions:
                self.clear_assertions()

    def contains(self, actual: Any, value: Any, **kwargs: Any):
        assertion = Assertion(self.contains.__name__, **kwargs)
        assertion.actual = actual
        assertion.expected = "Contains value"
        assertion.is_success = value in actual
        assertion.args.value = value
        return self.add_assertion(assertion)

    def empty(self, actual: Any, **kwargs: Any):
        assertion = Assertion(self.empty.__name__, **kwargs)
        assertion.actual = actual
        assertion.expected = "Length is 0"
        assertion.is_success = len(actual) == 0
        return self.add_assertion(assertion)

    def equals(self, actual: Any, expected: Any, **kwargs: Any):
        assertion = Assertion(self.equals.__name__, **kwargs)
        assertion.actual = actual
        assertion.expected = expected
        assertion.is_success = actual == expected
        return self.add_assertion(assertion)

    def true(self, actual: bool, **kwargs: Any):
        assertion = Assertion(self.true.__name__, **kwargs)
        assertion.actual = actual
        assertion.expected = True
        assertion.is_success = actual is assertion.expected
        return self.add_assertion(assertion)
