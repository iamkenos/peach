import os

from dotenv import load_dotenv
from behave.model import ScenarioOutline, Row
from iamkenos.peach import Context


def before_all(_):
    load_dotenv()


def before_feature(ctx: Context, feature):
    print("------------------------------------------------------------")
