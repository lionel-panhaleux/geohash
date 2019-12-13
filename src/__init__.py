import argparse
import csv
import sys
import geohash
import typing


def compute_prefixes(strings: typing.Iterable[str]):
    """Given an iterable of strings, returns a dict of unique shorter prefixes.

    Note in case of collision, the string is not included in the results, eg.:

    $> compute_prefixes(["foo", "foobar"])
    {"foobar": "foob"}
    """
    prefixes = {}
    for s in strings:
        for hashlen in range(1, len(s) + 1):
            prefix = s[:hashlen]
            if prefix not in prefixes:
                prefixes[prefix] = s
                break
            if not prefixes[prefix]:
                # this prefix is already shorter than another unique prefix
                continue
            # {prefix: string} -> {prefix: None, longer_prefix: string}
            # for parallelization, these write operations must be atomic as a whole
            prefixes[prefixes[prefix][: hashlen + 1]] = prefixes[prefix]
            prefixes[prefix] = None
    return {v: k for k, v in prefixes.items() if v}


def print_geohashes(source: typing.TextIO, dest: typing.TextIO = sys.stdout):
    """Given a CSV source with "lat,lng" (latitude, longitude), outputs a CSV
    with "lat,lng,geohash,uniq" (geohash, shortest unique geohash prefix).

    All points are output in input order, geohash has a 12 chars size.
    Two identical points (or close enough) will get
    the same full 12 chars geohash as "unique" shortest geohash prefix.
    """
    res = [
        (
            coordinates["lat"],
            coordinates["lng"],
            geohash.encode(float(coordinates["lat"]), float(coordinates["lng"])),
        )
        for coordinates in csv.DictReader(source)
    ]
    prefixes = compute_prefixes(r[2] for r in res)
    writer = csv.writer(dest)
    writer.writerow(["lat", "lng", "geohash", "uniq"])
    writer.writerows([(lat, lng, h, prefixes.get(h) or h) for lat, lng, h in res])


# #####################################################################################
# CLI

parser = argparse.ArgumentParser(
    prog="geohash",
    description="Compute geohash and unique shorter prefix (i/o in CSV format)",
)
parser.add_argument(
    "source",
    metavar="file",
    nargs="?",
    type=argparse.FileType(),
    default=sys.stdin,
    help=(
        "Input file in CVS format with 'lat' and 'lng' columns "
        "for latitude and longitude. If no file is provided, stdin is used."
    ),
)


def excepthook(type, value, traceback):
    """Do not display traceback on errors (eg. keyboard interrupt).
    """
    sys.stderr.write(str(value))


def main():
    """Command-line interface entry point.
    """
    sys.excepthook = excepthook
    print_geohashes(parser.parse_args().source)
