"""Prep __main__ entry."""
# pylint: disable=
from typing import Optional

import environs
import logzero
import typer
from icecream import ic
from icecream import install as ic_install
from logzero import logger

from too_short_url import __version__, too_st

# set env LOGLEVEL to 10/debug/DEBUG to turn on debug
try:
    _ = environs.Env().log_level("LOGLEVEL")
# except environs.EnvValidationError:
except (environs.EnvError, environs.EnvValidationError):
    _ = None
except Exception:
    _ = None
logzero.loglevel(_ or 10)
# logzero.loglevel(_ or 20)

# logger.debug(" debug: %s", __file__)
# logger.info(" info: %s", __file__)

ic_install()
ic.configureOutput(
    includeContext=True,
    # outputFunction=logger.info,
    outputFunction=logger.debug,
)
ic.enable()

app = typer.Typer(
    name="too-st",
    add_completion=False,
    help="Generate a too.st shorturl",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{app.info.name} v.{__version__}")
        raise typer.Exit()


@app.command()
def main(
    url: str = typer.Argument(..., help="url to be shortened"),
    keyword: str = typer.Option(
        "",
        "--keyword",
        "--kw",
        "-k",
        help="desired keyword, e.g. https://too.st/abc for KEYWORD set to abc",
        metavar="KEYWORD",
    ),  #
    best_effort: bool = typer.Option(
        False,
        "--best-effort",
        "--besteffort",
        "-b",
        is_flag=True,
        help="whether to try hard to generaet the desired shorturl https://too.st/KEYWORD",
    ),
    version: Optional[bool] = typer.Option(  # pylint: disable=(unused-argument
        None,
        "--version",
        "-v",
        "-V",
        help="Show version info and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
):
    """Generate too.st short url.

    e.g.

    * too-st baidu.com  # https://too.st/b

    * too-st baidu.com -k abc  # https://too.st/b

    * too-st baidu.com -k abc -b  # https://too.st/abc or https://too.st/b dependent on whether https://too.st/abc is already taken or reserved by th admin of too.st.

    """
    try:
        shorten_url = too_st(url, keyword, best_effort)
        typer.echo(shorten_url)
        raise typer.Exit()
    except Exception as e:
        typer.echo(e)
        raise typer.Exit()


if __name__ == "__main__":
    app()
