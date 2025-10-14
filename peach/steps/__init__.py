# pyright: reportCallIssue=false, reportRedeclaration=false, reportAssignmentType=false

from behave import step, then

from peach.fixtures.page import PageObject
from peach.plugins.context import Context
from peach.steps.expressions.expressions_steps import *
from peach.steps.parameter_types.parameter_types_steps import *


# ===========================================
#   samples for getting started
# ===========================================
class PlaywrightHomePage(PageObject):
    def __init__(self):
        super().__init__()
        self.url = "https://playwright.dev/python"
        self.nav = lambda: self.page.locator("//nav")
        self.nav_item = lambda label: self.nav().locator(f"//a[text()='{label}']")


@step("a condition is met")
def step_impl(ctx: Context):
    pg = PlaywrightHomePage()
    pg.navigate()


@step("an event is triggered")
def step_impl(ctx: Context):
    pass


@then("a condition is satisfied")
def step_impl(ctx: Context):
    pg = PlaywrightHomePage()
    pg.expect().url_contains("python").poll()


@then("a condition is not satisfied")
def step_impl(ctx: Context):
    """
    bunch of things happening below
    1. call expect on a locator and build expected conditions
    2. optionally set the exception prototype; anything other than an AssertionError will yield a broken test status
       this helps with narrowing down which failures are assertion / test failures and others
    3. optionally set an action to do before checking the built conditions
    4. set a `displayed` condition - this will check whether the locator is visible
    5. set a `true` condition - this will check that the value passed is `True` (which will always fail in the example below)
    6. finally call poll to keep trying both the action and the checks until the configured timeout is reached
    7. the `pg.nav().click()` won't execute, so this test is considered "broken" which is why we set a different
       exception prototyp on step 2 above

    this test should show the first assertion to pass and the second to fail because `False` would never be `True`
    """
    # fmt: off
    pg = PlaywrightHomePage()
    pg.nav_item("Node.js") \
        .expect() \
        .set_exception_type(TimeoutError) \
        .set_action(lambda: pg.nav_item("Python").first.hover()) \
        .displayed() \
        .true(False) \
        .poll()
    # fmt: on

    pg.nav().click()
