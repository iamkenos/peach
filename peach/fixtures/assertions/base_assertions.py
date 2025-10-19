import inspect
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Callable, Self, Type

from peach.utilities.object import format_obj
from peach.utilities.string import format_str

from ...fixtures import Fixture


class Assertion(object):
    assertion_is_successful: bool
    assertion_message: str
    expected: Any
    actual: Any

    def __init__(self, assertion_fn: Callable, *, is_not=False, message="", **kwargs):
        super().__init__()
        self.__sucess_criteria: Callable[[Self], bool] = lambda self=self: False
        self.__name: str = assertion_fn.__name__
        self.__message: str = message
        self.__is_not: bool = is_not
        self.__index: int = None
        self.__args: SimpleNamespace = SimpleNamespace(**kwargs)

    @property
    def args(self) -> SimpleNamespace:
        return self.__args

    def set_success_criteria(self, criteria: Callable[[Self], bool] | bool):
        self.__sucess_criteria = criteria

    def set_expected(self, expected: Any):
        self.expected = expected

    def set_actual(self, actual: Any):
        self.actual = actual

    def set_index(self, index: int):
        self.__index = index

    def evaluate(self):
        args = self.args.__dict__
        has_expected_value = hasattr(self, "expected")
        has_actual_value = hasattr(self, "actual")
        format = lambda v: format_str.indent(f"\n{format_obj.beautify(v)}") if isinstance(v, (list, dict)) else v  # noqa

        message_str = f"\nMessage: {self.__message}" if bool(self.__message) else ""
        expected_str = f"\nExpected{' (Not)' if self.__is_not else ''}: {format(self.expected)}" if has_expected_value else ""
        actual_str = f"\nActual: {format(self.actual)}" if has_actual_value else ""
        args_str = f"\n{format_obj.humanize(args)}" if args else ""

        criteria_result = self.__sucess_criteria(self) if callable(self.__sucess_criteria) else self.__sucess_criteria
        self.assertion_is_successful = criteria_result ^ self.__is_not  # flip if not
        self.assertion_message = f"""
Assertion #{self.__index + 1}: expect.{format_str.to_snake(self.__name)}(...)

Result: {"Success" if self.assertion_is_successful else "Failed"}{message_str}{expected_str}{actual_str}{args_str}
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
        self.__action: Callable[[Self], Any] = None
        self.__args: SimpleNamespace = SimpleNamespace(**kwargs)

    @property
    def args(self) -> SimpleNamespace:
        return self.__args

    @property
    def is_soft(self) -> bool:
        return self.__soft

    def set_action(self, callback: Callable[[Self], Any]):
        self.__action = callback
        return self

    def reset(self):
        self.soft(False)
        self.assertions = []

    def add_assertion(self, assertion: Assertion):
        assertion.set_index(len(self.assertions))
        self.assertions.append(assertion)
        return self

    def set_exception_type(self, e: Type[Exception] = Exception):
        self.ExceptionType = e
        return self

    def soft(self, state=True):
        self.__soft = state
        return self

    def evaluate(self, *, reset_state=True, **kwargs: Any):
        try:
            if self.__action:
                self.__action(self)
        except Exception:
            pass

        results = []
        for assertion in self.assertions:
            assertion: Assertion
            results.append(assertion.evaluate())

        failed_count = len(list(filter(lambda result: not result.assertion_is_successful, results)))
        total_count = len(self.assertions)
        message = ""
        is_success = failed_count == 0

        if not is_success:
            top_level_args = dict(**self.args.__dict__, **kwargs)
            top_level_args = f"\n{format_obj.humanize(top_level_args)}" if top_level_args else ""
            header = f"\nFailed on {failed_count}/{total_count} {format_str.to_lower(self.__name)}.{top_level_args}\n"
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
            if reset_state:
                self.reset()

    def contains(self, *, expected: Any, actual: Any, is_not=False, **kwargs: Any):
        assertion = Assertion(self.contains, is_not=is_not, **kwargs)
        assertion.set_expected("Contains value")
        assertion.set_actual(actual)
        assertion.set_success_criteria(lambda this: this.args.value in this.actual)
        assertion.args.value = expected
        return self.add_assertion(assertion)

    def equals(self, *, expected: Any, actual: Any, is_not=False, **kwargs: Any):
        assertion = Assertion(self.equals, is_not=is_not, **kwargs)
        assertion.set_expected(expected)
        assertion.set_actual(actual)
        assertion.set_success_criteria(expected == actual)
        return self.add_assertion(assertion)

    def empty(self, actual: Any, *, is_not=False, **kwargs: Any):
        assertion = Assertion(self.empty, is_not=is_not, **kwargs)
        assertion.set_expected("Length is 0")
        assertion.set_actual(actual)
        assertion.set_success_criteria(lambda this: 0 == this.actual)
        return self.add_assertion(assertion)

    def true(self, actual: bool, *, is_not=False, **kwargs: Any):
        assertion = Assertion(self.true, is_not=is_not, **kwargs)
        assertion.set_expected(True)
        assertion.set_actual(actual)
        assertion.set_success_criteria(lambda this: this.expected == this.actual)
        return self.add_assertion(assertion)

    def predicate(self, predicate: Callable[[], bool], *, is_not=False, **kwargs: Any):
        assertion = Assertion(self.predicate, is_not=is_not, **kwargs)
        assertion.set_success_criteria(lambda _: predicate())
        assertion.args.predicate = inspect.getsource(predicate).strip().rstrip(",")
        return self.add_assertion(assertion)
