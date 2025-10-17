from behave.model import Feature, Scenario, Step

from peach.plugins.context import Context, extend


def before_all(ctx: Context):
    extend(ctx)
    ctx.hooks.before_all()


def before_feature(ctx: Context, feature: Feature):
    pass


def before_scenario(ctx: Context, scenario: Scenario):
    ctx.hooks.set_scenario_identifier_hash(scenario)
    ctx.hooks.suffix_scenario_name_with_example_id(scenario)


def after_scenario(ctx: Context, scenario: Scenario):
    ctx.hooks.close_browser_page()
    ctx.hooks.delete_scenario_browser_recording_on_sucess(scenario)
    ctx.hooks.delete_scenario_log_file_if_empty()


def after_step(ctx: Context, step: Step):
    ctx.hooks.attach_evidences_on_error(step)


def after_all(ctx: Context):
    ctx.hooks.after_all()
