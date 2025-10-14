import click


@click.group()
def cli():
    pass


@cli.command()
def init():
    # TODO: add quick start utility here
    print("Running init...")
