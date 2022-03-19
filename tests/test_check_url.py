"""Test check_url."""
import pytest
from too_short_url.check_url import check_url


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("abc.com", "http://abc.com"),
        ("ht:/abc.com", "http://abc.com"),
        ("ht:/abc.com", "http://abc.com"),
        (":/abc.com", "http://abc.com"),
        ("a:abc.com", "http://abc.com"),
        ("ftp://abc.com", "http://abc.com"),
    ],
)
def test_check_url(test_input, expected):
    """Test check_url."""
    assert check_url(test_input) == expected


@pytest.mark.xfail
def test_check_url_fail():
    check_url("com")


@pytest.mark.xfail
def test_check_url_1fail():
    check_url(".com")
