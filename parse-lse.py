#!/usr/bin/env python3

import argparse
import datetime
import json
import pathlib
import re
from typing import Dict
from urllib import request

Prices = Dict[str, str]


def parse_response(existing_prices: dict, response: dict) -> Prices:
    prices = {}

    for entry in response['d']:
        date = datetime.datetime.fromtimestamp(entry[0] / 1000).strftime('%Y-%m-%d')
        price = '{0:.3f}'.format(entry[1] / 100)

        if date not in existing_prices:
            prices[date] = price

    return prices


def parse_args():
    parser = argparse.ArgumentParser(description='Parse historic commodity prices from the London Stock Exchange.')
    parser.add_argument('key', help='The commodity key, e.g. "UKX.FTD" for FTSE100')
    parser.add_argument('commodity', help='The commodity name, e.g. FTSE100')
    parser.add_argument('-c', '--currency', default='GBP', help='The currency of the price, defaults to "GBP"')
    parser.add_argument('file', help='The beancount price file, e.g. FTSE100.beancount')
    return parser.parse_args()


def read_prices(file: str, commodity: str, currency: str) -> Prices:
    path = pathlib.Path(file)
    price_pattern = re.compile('(\d{4}-\d{2}-\d{2}) price ' + commodity + ' (\d*\.?\d+) ' + currency)

    recorded_prices = {}

    if path.is_file():
        with open(path, 'r') as lines:
            for line in lines:
                match = re.search(price_pattern, line)
                if match:
                    recorded_prices[match.group(1)] = match.group(2)
            print('Read {} recorded price(s).'.format(len(recorded_prices)))

    return recorded_prices


def fetch_prices(key: str) -> dict:
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


def write_prices(file: str, prices: dict, commodity: str, currency: str) -> None:
    with open(file, 'a') as out:
        for date, price in prices.items():
            out.write(date + ' price ' + commodity + ' ' + price + ' ' + currency)
            out.write('\n')
    print('Wrote {} new price(s).'.format(len(prices)))


def run() -> None:
    args = parse_args()
    recorded_prices = read_prices(args.file, args.commodity, args.currency)
    response = fetch_prices(args.key)
    prices = parse_response(recorded_prices, response)

    if len(prices) == 0:
        print('Stock Exchange returned no unrecorded prices. Try again later.')
    else:
        write_prices(args.file, prices, args.commodity, args.currency)


run()
