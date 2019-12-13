[![Python version](https://img.shields.io/badge/python-3.7-blue)](https://www.python.org/downloads/release/python-375/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

# Geohash

This is a [geohash](http://geohash.org) tool in
[python 3](https://www.python.org/downloads/release/python-375/).
Given a [CSV](https://tools.ietf.org/html/rfc4180)
file containing latitudes and longitudes,
it provides the geohash and the shortest unique geohash for each point.

For instance, the three points below will give:

| latitude        | longitude       | geohash      | unique_prefix |
| --------------- | --------------- | ------------ | ------------- |
| 41.388828145321 | 2.1689976634898 | sp3e3qe7mkcb | sp3e3         |
| 41.390743       | 2.138067        | sp3e2wuys9dr | sp3e2wuy      |
| 41.390853       | 2.138177        | sp3e2wuzpnhr | sp3e2wuz      |

## Setup

Clone or download the repository, then:

```bash
pip install -e .
```

To run the tests, install the `dev` version and use
[pytest](https://docs.pytest.org/en/latest/):

```bash
pip install -e .[dev]
pytest
```

## Usage

Given a well-formated CSV file:

```csv
lat,lng
41.388828145321,2.1689976634898
41.390743,2.138067
41.390853,2.138177
```

The `geohash` command line will output the following CSV on the standard output:

```bash
$> geohash example.csv
lat,lng,geohash,uniq
41.388828145321,2.1689976634898,sp3e3qe7mkcb,sp3e3
41.390743,2.138067,sp3e2wuys9dr,sp3e2wuy
41.390853,2.138177,sp3e2wuzpnhr,sp3e2wuz
```

## Design notes

- CSV output uses `CR+LF` (`"\r\n"`) line endings
  (as per CSV [RFC4180](https://tools.ietf.org/html/rfc4180))
- The `geohash` command can also use the standard input instead of a file.
- Geohash precision is set to 12 characters (usual default).
- Order is stable: all points are output in the input order.
- If two points have the same geohash,
  the full geohash is the _"shorter unique"_ geohash for both.
- The code is formatted using [black](https://pypi.org/project/black/)
  and linted with [flake8](https://pypi.org/project/flake8/).
