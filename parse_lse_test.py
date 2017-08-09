from parse_lse import diff_prices, parse_response


def test_parse_empty_response() -> None:
    prices = parse_response({'d': []})
    assert prices == {}


def test_parse_response() -> None:
    response = {
        'd': [
            [1420070400000, 510.500],
            [1511327045000, 202.150],
        ]
    }

    prices = parse_response(response)

    assert prices == {
        '2015-01-01': '5.105',
        '2017-11-22': '2.022'
    }


def test_diff_prices() -> None:
    existing = {
        '2016-01-01': '10.021',
        '2010-12-25': '732.159',
        '1995-08-17': '3024.568'
    }

    new = {
        '2010-12-25': '804.344',
        '2017-08-24': '6.347',
        '1995-08-17': '3024.568'
    }

    prices = diff_prices(existing, new)

    assert prices == {'2017-08-24': '6.347'}
