#
# (c) 2025 Yoichi Tanibayashi
#
import click
from pyclickutils import click_common_opts, get_logger

from . import __version__
from .pyclibase import CliBase


@click.command(name=__package__)
@click.option(
    "--history-file", type=str, default="/tmp/hist", show_default=True, help="history file"
)
@click.option(
    "--script-file",
    "-f",
    type=str,
    default="",
    help="script file",
)
@click_common_opts(click, __version__)
def main(ctx, history_file, script_file, debug):
    """CLI main."""
    my_name = ctx.command.name
    log = get_logger(__name__, debug)
    log.debug(
        "my_name=%a, history_file=%s, script_file=%s",
        my_name, history_file, script_file
    )

    cli = CliBase(my_name, history_file, script_file=script_file, debug=debug)
    cli.main()
