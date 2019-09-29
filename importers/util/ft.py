from .rest import post


def get_prices(label: str, symbol: str) -> dict:
    return post('https://markets.ft.com/data/chartapi/series', {
        'days': 3650,
        'dataNormalized': False,
        'dataPeriod': 'Month',
        'dataInterval': 1,
        'endOffsetDays': 0,
        'exchangeOffset': 0,
        'realtime': False,
        'yFormat': '0.###',
        'timeServiceFormat': 'JSON',
        'rulerIntradayStart': 26,
        'rulerIntradayStop': 3,
        'rulerInterdayStart': 10957,
        'rulerInterdayStop': 365,
        'returnDateType': 'ISO8601',
        'elements': [
            {
                'Label': label,
                'Type': 'price',
                'Symbol': symbol,
                'OverlayIndicators': [],
                'Params': {}
            }
        ]
    })
