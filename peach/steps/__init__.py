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
    pg = PlaywrightHomePage()

    # optionally set the exception prototype; anything other than an AssertionError will yield a broken test status
    # helps with narrowing down which failures are assertion / test failures and others
    pg.nav().expect().set_exception_type(Exception).displayed().true(False).poll()
