import backoff

from peach.fixtures.attributes.env import DEFAULT_TIMEOUT

from ..base_assertions import BaseAssertions, SimpleNamespace


class PolledAssertions(BaseAssertions):
    def __init__(self, *, timeout: int = DEFAULT_TIMEOUT, **kwargs):
        super().__init__(**kwargs)
        self.__timeout: int = timeout

    def poll(self, max_tries: int | None = None, timeout: int | None = None):
        tries = SimpleNamespace(**dict(count=0, elapsed=0, has_givenup=False))
        timeout = timeout or self.__timeout

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
            on_success=lambda _: self.reset(),
            on_giveup=on_giveup,
        )
        def poll():
            return self.evaluate(
                reset_state=False,
                polling_status=f"Timed out after {tries.count} attempts over {int(tries.elapsed)} seconds.",
            )

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
                self.reset()
                raise E
        finally:
            # reset soft assertions back it back to its original state
            self.soft(should_return_soft_assertion_result)
