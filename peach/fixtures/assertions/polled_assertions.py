# pyright: reportIncompatibleVariableOverride=false
from typing import Callable

import backoff

from peach.fixtures.attributes.env import DEFAULT_TIMEOUT

from .base_assertions import Any, Assertion, BaseAssertions, SimpleNamespace


class PolledAssertion(Assertion):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.actual_predicate: Callable[[], Any]
        self.is_success_predicate: Callable[[], bool]

    @property
    def actual(self) -> Any:
        return self.actual_predicate()

    @property
    def is_success(self) -> bool:
        return self.is_success_predicate()

    @is_success.setter
    def is_success(self, value):
        self.is_success_predicate = value


class PolledAssertions(BaseAssertions):
    def __init__(self, timeout: int, **kwargs):
        super().__init__(**kwargs)
        self.timeout = timeout or DEFAULT_TIMEOUT

    def poll(self, max_tries=None, timeout=None):
        tries = SimpleNamespace(**dict(count=0, elapsed=0, has_givenup=False))
        timeout = timeout or self.timeout

        def giveup(_):
            if max_tries and tries.count >= max_tries:
                return True
            elif timeout and tries.elapsed >= timeout:
                return True
            return False

        def on_backoff(details):
            backoff_details = SimpleNamespace(**details)
            tries.count = backoff_details.tries
            tries.elapsed = backoff_details.elapsed

        def on_giveup(details):
            tries.has_givenup = True

        @backoff.on_exception(
            backoff.constant,
            self.ExceptionType,
            backoff_log_level=0,
            giveup_log_level=0,
            giveup=giveup,
            on_backoff=on_backoff,
            on_success=lambda _: self.clear_assertions(),
            on_giveup=on_giveup,
        )
        def poll():
            return self.evaluate(clear_assertions=False, polling_status=f"Timed out after {tries.count} attempts over {int(tries.elapsed)} seconds.")

        # turn off soft assertions so errors are always thrown on failure and backoff is fired accordingly
        # this is so soft assertions are properly retried and dont resolve immediately if they fail
        should_return_soft_assertion_result = self.is_soft
        self.soft(False)
        try:
            return poll()
        except Exception as E:
            if tries.has_givenup and should_return_soft_assertion_result:
                return self.soft().evaluate()
            else:
                self.clear_assertions()
                raise E
        finally:
            # reset soft assertions back it back to its original state
            self.soft(should_return_soft_assertion_result)
