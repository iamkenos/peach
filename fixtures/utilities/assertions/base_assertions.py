from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from fixtures.utilities.formatters import json_formatter, string_formatter


class Colors:
    RED = "\033[91m"
    RESET = "\033[0m"


class Assertion(object):
    def __init__(self, name: str, **kwargs):
        is_not, message = "is_not", "message"
        self.message: str = kwargs.get(message, "")
        self.is_not: bool = kwargs.get(is_not, False)
        self.is_success: bool = False
        self.index: int = None
        self.name = string_formatter.to_sentence_case(f"{'not ' if self.is_not else ''}{name}")
        self.__args: SimpleNamespace = SimpleNamespace(**{key: value for key, value in kwargs.items() if key not in [is_not, message]})

    @property
    def args(self) -> SimpleNamespace:
        return self.__args

    def __beautify_arg_value(self, value):
        return string_formatter.indent(f"\n{json_formatter.beautify(value)}") if isinstance(value, (list, dict)) else value

    def __beautify_args(self, kwargs: dict):
        args: list = []
        for key, value in kwargs.items():
            prop = string_formatter.to_sentence_case(key)
            value = self.__beautify_arg_value(value)
            args.append(f"\n{prop}: {value}")
        args_string = "".join(args) if args else ""
        return args_string

    def check(self):
        args = self.args.__dict__
        has_expected_value = hasattr(self, "expected")
        has_actual_value = hasattr(self, "actual")
        expected_str = f"\nExpected {self.name.lower()}: {self.__beautify_arg_value(self.expected)}" if has_expected_value else ""
        actual_str = f"\nActual: {self.__beautify_arg_value(self.actual)}" if has_actual_value else ""
        message_str = f"\nMessage: {self.message}" if bool(self.message) else ""

        self.is_success = not self.is_success if self.is_not else self.is_success
        self.message = f"""
Assertion #{self.index + 1}: {self.name}

Result: {"Success" if self.is_success else "Failed"}{actual_str}{expected_str}{message_str}{self.__beautify_args(args)}
""".strip()
        self.message = string_formatter.indent(f"\n{self.message}")
        return self


@dataclass
class Result:
    results: list[Assertion]
    is_success: bool
    message: str


class BaseAssertions(object):
    def __init__(self, **kwargs):
        self._ctx = None
        self.assertions: list[Assertion] = []
        self.name = kwargs.get("name", self.__class__.__name__).title()
        self.is_soft = kwargs.get("is_soft", False)
        self.result: Result = None
        self.__args: SimpleNamespace = SimpleNamespace(**kwargs)

    @property
    def args(self) -> SimpleNamespace:
        return self.__args

    def add_assertion(self, assertion: Assertion):
        assertion.index = len(self.assertions)
        self.assertions.append(assertion)
        return self

    def evaluate(self):
        results = []
        for assertion in self.assertions:
            assertion: Assertion
            results.append(assertion.check())

        failed_count = len(list(filter(lambda result: not result.is_success, results)))
        total_count = len(self.assertions)
        message = ""
        is_success = failed_count == 0

        if not is_success:
            header = f"\nFailed on {failed_count}/{total_count} assertions.\n"
            body = "\n  --------------------------------".join(map(lambda result: result.message, results))
            message = f"{Colors.RED}{header}{body}{Colors.RESET}"

        self.result = Result(results=results, is_success=is_success, message=message)
        try:
            if not self.is_soft and not self.result.is_success:
                raise AssertionError(self.result.message)
            else:
                return self.result.is_success
        finally:
            self.assertions = []

    def contains(self, actual: Any, value: Any, **kwargs):
        assertion = Assertion(self.contains.__name__, **kwargs)
        assertion.actual = actual
        assertion.expected = value
        assertion.is_success = value in actual
        return self.add_assertion(assertion)

    def empty(self, actual: Any, **kwargs):
        assertion = Assertion(self.empty.__name__, **kwargs)
        assertion.actual = actual
        assertion.is_success = len(actual) == 0
        return self.add_assertion(assertion)

    def equals(self, actual: Any, expected: Any, **kwargs):
        assertion = Assertion(self.equals.__name__, **kwargs)
        assertion.actual = actual
        assertion.expected = expected
        assertion.is_success = actual == expected
        return self.add_assertion(assertion)

    def true(self, actual: bool, **kwargs):
        assertion = Assertion(self.true.__name__, **kwargs)
        assertion.actual = actual
        assertion.is_success = actual == True  # noqa: E712
        return self.add_assertion(assertion)
