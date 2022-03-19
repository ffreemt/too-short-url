"""Return a shorturl based on too.st."""
# pylint: disable=invalid-name

from random import sample
from string import ascii_letters
import re
import brotli
import httpx
from httpx import Timeout
from logzero import logger
from furl import furl
import validators
from pyquery import PyQuery as pq

from .check_url import check_url

headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Referer": "https://too.st/",
    "Accept-encoding": "gzip, deflate, br",
}
too_st_url = "https://too.st"


def _too_st(
    url: str,
    keyword: str = "",
    best_effort: bool = False,
    timeout: Timeout = Timeout(15),
) -> str:
    """Get a shorturl."""
    try:
        resp = httpx.post(
            too_st_url,
            data=dict(url=url, keyword=keyword),
            headers=headers,
            timeout=Timeout(15),
            verify=False,
            # trust_env=False,
        )
        resp.raise_for_status()
    except Exception as e:
        logger.error(e)
        raise

    # known to be br compression
    try:  # httpx 22.0 already decompressed
        text = resp.text
    except UnicodeDecodeError:  # early httpx
        try:
            text = brotli.decompress(resp.content).decode()
        except Exception as e:
            logger.error(e)
            raise

    _too_st.text = text

    res = re.findall(r"https://too.st/\w+", text)

    if res:
        return res[0]

    # return text
    doc = pq(text)
    out = doc(".field-section").text()
    if out:
        out = out.splitlines()[0]
    else:
        out = doc(".main-content").text()

    return out if out.strip() else "Something is wrog..."


def too_st(
    url: str,
    keyword: str = "",
    best_effort: bool = False,
    timeout: Timeout = Timeout(15),
) -> str:
    """Run _too_st with some error-checking."""
    try:
        url_c = check_url(url)
    except Exception as e:
        logger.error(e)
        raise

    if " " in keyword.strip():
        logger.warning("Does not make much sense to have a space there, removed")
        keyword = keyword.strip().replace(" ", "")

    try:
        res = _too_st(url_c, keyword, best_effort, timeout)
    except Exception as e:
        logger.error(e)
        raise

    if not keyword:
        if validators.url(res):
            return res
        else:
            # this ought not happen
            raise Exception(
                "Something is night right, we don't know why tho. Maybe too.st ceases to operate."
            )

    # keyword specified
    if not best_effort:  # deliver whatever we got
        if validators.url(res):
            return res
        else:
            raise Exception(
                " The shorturl desired can't be obtained maybe it's already cached or reserved by too.st."
            )

    # best_effort set to True and keyword specified
    # ===

    # the returned shorturl is not the keyword given
    # the url has been given previously
    # attache st_tag=random-string and retry

    if validators.url(res):
        f_url = furl(url_c)
        tag = "".join(sample(ascii_letters, 4))

        # update query
        f_url.query.add({"sttag": tag})

        # will not recheck
        return _too_st(f_url.url, keyword=keyword, timeout=timeout)

    raise Exception(" Well, bad luck, something fishy. is happening..")
