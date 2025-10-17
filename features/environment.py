from behave.cucumber_expression import use_step_matcher_for_cucumber_expressions
from behave.model import Feature, Scenario, Step

from peach import environment
from peach.plugins.context import Context

use_step_matcher_for_cucumber_expressions()


def before_all(ctx: Context):
    environment.before_all(ctx)


def before_feature(ctx: Context, feature: Feature):
    environment.before_feature(ctx, feature)


def before_scenario(ctx: Context, scenario: Scenario):
    environment.before_scenario(ctx, scenario)


def before_step(ctx: Context, step: Step):
    environment.before_step(ctx, step)


def after_step(ctx: Context, step: Step):
    environment.after_step(ctx, step)


def after_scenario(ctx: Context, scenario: Scenario):
    environment.after_scenario(ctx, scenario)


def after_feature(ctx: Context, feature: Feature):
    environment.after_feature(ctx, feature)


def after_all(ctx: Context):
    environment.after_all(ctx)
