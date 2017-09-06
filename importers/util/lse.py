from .rest import post


def get_prices(key: str) -> dict:
    return post('http://charts.londonstockexchange.com/WebCharts/services/ChartWService.asmx/GetPrices', {
        'request': {
            'SampleTime': '1d',
            'TimeFrame': '5y',
            'RequestedDataSetType': 'ohlc',
            'ChartPriceType': 'price',
            'Key': key,
            'OffSet': 0,
            'FromDate': None,
            'ToDate': None,
            'UseDelay': True,
            'KeyType': 'Topic',
            'KeyType2': 'Topic',
            'Language': 'en'
        }
    })
