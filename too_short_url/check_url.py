"""Check and fix url."""
import validators
from furl import furl

from logzero import logger


def check_url(url: str) -> str:
    """Check and fix url provided."""
    flag = False
    if not validators.url(url):
        logger.warning(" url (%s) is not valid", url)
        logger.info("We try to fix it.")
        flag = True

    f_url = furl(url)

    if f_url.host is None and f_url.scheme is None:
        # probably missing scheme, add http://
        f_url = furl(f"http://{url}")

    if f_url.host is not None:
        if "." not in f_url.host:  # reject top level domain
            raise Exception(
                "Not a valid url in the most common sense, cant fix it for you." ""
            )

    # probably misspelt scheme
    # add http:// to host or path.segments
    if f_url.scheme.lower() not in ["http", "https"]:
        if f_url.scheme.lower() in ["ftp", "file", "file:///"]:
            logger.warning(
                " too.st only supports http:// and https://, we simply change it to http://"
            )
        _ = f_url.host or "".join(f_url.path.segments)
        f_url = furl(f"http://{_}")

    if validators.url(f_url.url):
        if flag:
            logger.info("Fixed url: %s", f_url.url)
        return f_url.url

    raise Exception("Unable to fix, sorry.")
