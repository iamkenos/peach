# pyright: reportCallIssue=false, reportRedeclaration=false

from behave import step, then

from peach.fixtures.assertions import Assertions
from peach.plugins.context import Context


# ===========================================
#   samples for cucumber expressions
# ===========================================
# see: https://behave.readthedocs.io/en/stable/appendix.cucumber_expressions/#example
# caveat: word alternatives are not supported by some code editor plugins
# so albeit verbose, stacking definitions sometimes give better developer experience.
@step("a user does {int} action")
@step("a user does {int} actions")
@step("an administrator does {int} action")
@step("an administrator does {int} actions")
def step_impl(ctx: Context, count: int):
    ctx.parameters.count_of_actions = count


@then("a total of {int} action is performed")
@step("a total of {int} actions are performed")
def step_impl(ctx: Context, count: int):
    expect = Assertions()
    expect.equals(actual=ctx.parameters.count_of_actions, expected=count).evaluate()
