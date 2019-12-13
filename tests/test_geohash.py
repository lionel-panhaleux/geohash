import io
import src


def test_compute_prefixes():
    """Test the core compute_prefixes function
    """
    assert src.compute_prefixes(["foo", "bar", "baz"]) == {
        "foo": "f",
        "bar": "bar",
        "baz": "baz",
    }
    assert src.compute_prefixes(["foo", "foo"]) == {}
    assert src.compute_prefixes(["foo", "foobar"]) == {"foobar": "foob"}


def test_print_geohashes():
    """Test provided short example
    """
    out = io.StringIO()
    src.print_geohashes(open("tests/files/test.csv"), out)
    assert out.getvalue() == (
        "lat,lng,geohash,uniq\r\n"
        "41.388828145321,2.1689976634898,sp3e3qe7mkcb,sp3e3\r\n"
        "41.390743,2.138067,sp3e2wuys9dr,sp3e2wuy\r\n"
        "41.390853,2.138177,sp3e2wuzpnhr,sp3e2wuz\r\n"
    )


def test_print_geohashes_with_collision():
    """Test result when two points are identical in the file
    """
    out = io.StringIO()
    src.print_geohashes(open("tests/files/test_duplicates.csv"), out)
    assert out.getvalue() == (
        "lat,lng,geohash,uniq\r\n"
        "41.388828145321,2.1689976634898,sp3e3qe7mkcb,sp3e3\r\n"
        "41.390743,2.138067,sp3e2wuys9dr,sp3e2wuys9dr\r\n"
        "41.390853,2.138177,sp3e2wuzpnhr,sp3e2wuz\r\n"
        "41.390743,2.138067,sp3e2wuys9dr,sp3e2wuys9dr\r\n"
    )
