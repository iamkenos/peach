from behave.cucumber_expression import use_step_matcher_for_cucumber_expressions
from behave.model import Feature, Scenario, Step

from fixtures.context import Context, extend

use_step_matcher_for_cucumber_expressions()


def before_all(ctx: Context):
    extend(ctx)
    ctx.hooks.before_all()


def before_feature(ctx: Context, feature: Feature):
    pass


def before_scenario(ctx: Context, scenario: Scenario):
    ctx.hooks.prefix_scenario_name_with_example_id(scenario)


def after_step(ctx: Context, step: Step):
    ctx.hooks.on_step_error(step, ctx.hooks.attach_evidences)


def after_all(ctx: Context):
    ctx.hooks.after_all()
