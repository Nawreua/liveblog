import pytest

import client

def test_parse_int():
    x = client.parse(['10'], [int])
    assert x == 10

def test_parse_multiple_int():
    x, y = client.parse(['5', '7'], [int, int])
    assert x == 5 and y == 7

def test_parse_multiple_type():
    x, s, f = client.parse(['4', 'test', '3.14'], [int, str, float])
    assert x == 4 and s == 'test' and f == pytest.approx(3.14)

def test_parse_error():
    with pytest.raises(ValueError):
        client.parse(['1', '*'], [int, int])
