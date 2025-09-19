from behave import step, then

from fixtures.context import Context
from fixtures.utilities.assertions import Assertions
from steps.expressions.expressions_steps import *
from steps.parameter_types.parameter_types_steps import *


# ===========================================
#   samples for getting started
# ===========================================
@step("a condition is met")
def step_impl(ctx: Context):
    ctx.browser.navigate("https://playwright.dev/python")


@step("an event is triggered")
def step_impl(ctx: Context):
    pass


@then("a condition is satisfied")
def step_impl(ctx: Context):
    expect = Assertions()
    expect.contains(actual=ctx.browser.page.url, value="python").evaluate()


@then("a condition is not satisfied")
def step_impl(ctx: Context):
    expect = Assertions()
    expect.contains(actual=ctx.browser.page.url, value="python", is_not=True).true(False).evaluate()
