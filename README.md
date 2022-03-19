# too-short-url
[![pytest](https://github.com/ffreemt/too-short-url/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/too-short-url/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/too-short-url.svg)](https://badge.fury.io/py/too-short-url)

shorturl based on too.st

## Install it
```bash
pip install too-short-url

# or pip install git+https://github.com/ffreemt/too-short-url
# or clone the repo and
```

## Use it

### Command line
```bash
too-st http://baid.com
# too.st/b

```

### With in `python`
```python
from too_short_url import too_st

print(too_st("http://baidu.com"))
# too.st/b
```

### Docs
```bash
too-st --help

Usage: too-st [OPTIONS] URL

  Generate too.st short url.

  e.g.

  * too-st baidu.com  # https://too.st/b

  * too-st baidu.com -k abc  # https://too.st/b

  * too-st baidu.com -k abc -b  # https://too.st/abc or https://too.st/b
  dependent on whether https://too.st/abc is already taken or reserved by th
  admin of too.st.

Arguments:
  URL  url to be shortened  [required]

Options:
  -k, --keyword, --kw KEYWORD     desired keyword, e.g. https://too.st/abc for
                                  KEYWORD set to abc
  -b, --best-effort, --besteffort
                                  whether to try hard to generaet the desired
                                  shorturl https://too.st/KEYWORD
  -v, -V, --version               Show version info and exit.
  --help                          Show this message and exit.
```
