import json
from urllib import request


def get_prices(key: str) -> dict:
    url = 'http://charts.londonstockexchange.com/WebCharts/services/ChartWService.asmx/GetPrices'

    data = {
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
    }

    headers = {
        'Content-Type': 'application/json'
    }

    req = request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    resp = request.urlopen(req)
    return json.loads(resp.read().decode())
