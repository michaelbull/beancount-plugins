import csv
import re
from datetime import date, datetime
from os import path
from typing import List, Optional

from beancount.core.amount import Amount
from beancount.core.data import Price, new_metadata
from beancount.core.number import D
from beancount.ingest.cache import _FileMemo
from beancount.ingest.importer import ImporterProtocol

from importers.util import post


def parse_iso8601(iso8601: str) -> date:
    return datetime.strptime(iso8601, '%Y-%m-%dT%H:%M:%S').date()


def parse_dates(dates: List[str]) -> List[date]:
    return list(map(parse_iso8601, dates))


def find_series_by_type(series_type: str, series: List[dict]) -> Optional[dict]:
    return next((x for x in series if x['Type'] == series_type), None)


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


class Importer(ImporterProtocol):
    """Importer for Financial Times market data."""

    def __init__(self, currency: str) -> None:
        self.currency = currency

    def identify(self, file: _FileMemo) -> bool:
        return path.basename(file.name).endswith('.price')

    def extract(self, file: _FileMemo, existing_entries=None) -> List[Price]:
        commodity = re.sub(r'\.price$', '', path.basename(file.name))
        prices = []
        entry = 1

        with open(file.name) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')

            for row in reader:
                label = row['Label']
                symbol = row['Symbol']

                response = get_prices(label, symbol)

                dates = response['Dates']
                elements = response['Elements']

                parsed_dates = parse_dates(dates)

                for element in elements:
                    series = element['ComponentSeries']
                    close = find_series_by_type('Close', series)

                    if close is not None:
                        values = close['Values']

                        for idx, value in enumerate(values):
                            price = Price(
                                meta=new_metadata(file.name, entry),
                                date=parsed_dates[idx],
                                currency=commodity,
                                amount=Amount(D('{0:.3f}'.format(value)), self.currency)
                            )

                            prices.append(price)
                            entry += 1

        return prices
