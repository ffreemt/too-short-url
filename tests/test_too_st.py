"""Test _too_st."""
from logzero import logger
from too_short_url.too_st import _too_st, too_st


def test_too_st0_google():
    """Test _too_st google."""
    url = "http://google.com"

    # keyword: str = ""
    # best_effort: bool = False
    # timeout: Timeout = Timeout(15)
    assert _too_st(url) == "https://too.st/2l"


def test_too_st0_baidu():
    """Test _too_st baidu."""
    url = "http://baidu.com"

    assert _too_st(url) == "https://too.st/b"


def test_too_st_baidu():
    """Test _too_st baidu."""
    url = "http://baidu.com"
    assert too_st(url) == "https://too.st/b"


def test_too_st_baidu_noscheme():
    """Test _too_st baidu."""
    url = "http://baidu.com"
    url = "baidu.com"

    assert too_st(url) == "https://too.st/b"
