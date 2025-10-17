from behave.model import Feature, Scenario, Step

from peach.fixtures.hooks.after_all import AfterAll
from peach.fixtures.hooks.after_feature import AfterFeature
from peach.fixtures.hooks.after_scenario import AfterScenario
from peach.fixtures.hooks.after_step import AfterStep
from peach.fixtures.hooks.before_all import BeforeAll
from peach.fixtures.hooks.before_feature import BeforeFeature
from peach.fixtures.hooks.before_scenario import BeforeScenario
from peach.fixtures.hooks.before_step import BeforeStep
from peach.plugins.context import Context, extend


def before_all(ctx: Context):
    extend(ctx)
    BeforeAll().run()


def before_feature(ctx: Context, feature: Feature):
    BeforeFeature(feature).run()


def before_scenario(ctx: Context, scenario: Scenario):
    BeforeScenario(scenario).run()


def before_step(ctx: Context, step: Step):
    BeforeStep(step).run()


def after_step(ctx: Context, step: Step):
    AfterStep(step).run()


def after_scenario(ctx: Context, scenario: Scenario):
    AfterScenario(scenario).run()


def after_feature(ctx: Context, feature: Feature):
    AfterFeature(feature).run()


def after_all(ctx: Context):
    AfterAll().run()
