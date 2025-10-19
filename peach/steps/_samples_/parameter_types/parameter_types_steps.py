# pyright: reportCallIssue=false, reportRedeclaration=false

from enum import Enum

from behave import step, then
from behave.cucumber_expression import TypeBuilder, define_parameter_type_with

from peach.fixtures.assertions import Assertions
from peach.plugins.context import Context


class Direction(Enum):
    up = 1
    right = 2
    left = 3
    down = 4


define_parameter_type_with(name="direction", regexp="up|right|left|down", type=Direction, transformer=TypeBuilder.make_enum(Direction))


# ===========================================
#   samples for custom parameter types
# ===========================================
# see: https://behave.readthedocs.io/en/stable/appendix.cucumber_expressions/#user-defined-types
@step("an actor goes {direction}")
def step_impl(ctx: Context, direction: Direction):
    ctx.parameters.last_direction = direction.name


@then("the actor's last known position is {direction}")
def step_impl(ctx: Context, direction: Direction):
    expect = Assertions()
    expect.equals(
        expected=direction.name,
        actual=ctx.parameters.last_direction,
        message="Verify the last known position of the actor.",
    ).evaluate()
