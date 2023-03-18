import inspect

import click

from .utils import dynamic_import
from ..environment import EnvironmentConfig


@click.group()
def main() -> None:
    pass


@main.group()
def env() -> None:
    pass


@env.command("show")
@click.option(
    "--config-module-path",
    required=True,
    help="python module path to root environment config",
)
def show_env(config_module_path: str) -> None:
    ConfigClass = dynamic_import(config_module_path)
    if not inspect.isclass(ConfigClass) or not issubclass(
        ConfigClass, EnvironmentConfig
    ):
        raise click.UsageError(
            f'"{config_module_path}" is not valid '
            "subclass of EnvironmentConfig"
        )
    variables = ConfigClass.get_all_variables()
    for v in variables:
        click.echo(f"\"{v.key}\" {'optional' if v.optional else 'required'}")
