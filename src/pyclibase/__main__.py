#
# (c) 2025 Yoichi Tanibayashi
#
import click
from pyclickutils import click_common_opts, get_logger

from . import __version__
from .pyclibase import CliBase


@click.command(name=__package__)
@click.option(
    "--script",
    "-f",
    type=str,
    default="",
    show_default=True,
    help="script file",
)
@click_common_opts(click, __version__)
def main(ctx, script, debug):
    """CLI main."""
    command_name = ctx.command.name
    log = get_logger(__name__, debug)
    log.debug("command_name=%a", command_name)
    log.debug("script=%s", script)

    cli = CliBase(command_name, "/tmp/hist", infile=script, debug=debug)
    if script:
        cli.run_file()
    else:
        cli.loop()
