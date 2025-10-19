from typing import Self

from peach.fixtures.services.types import RequestSpec, Response

from ..base_assertions import Any, Assertion
from . import PolledAssertions


class ApiAssertions(PolledAssertions):
    def __init__(self, request: RequestSpec, **kwargs):
        super().__init__(timeout=self._ctx.env.api_request_timeout, **kwargs)
        self.__request: RequestSpec = request
        self.__response: Response = None
        self.__set_action()

    @property
    def response(self):
        return self.__response

    def __set_action(self):
        def callback(this: Self):
            this.__response = self.__request.send()

        self.set_action(callback)

    def status_code_equals(self, expected: int, *, is_not=False, **kwargs: Any):
        def success_criteria(this: Assertion):
            this.set_actual(self.response.status_code)
            return this.expected == this.actual

        assertion = Assertion(self.status_code_equals, is_not=is_not, **kwargs)
        assertion.set_expected(expected)
        assertion.set_success_criteria(success_criteria)
        return self.add_assertion(assertion)
