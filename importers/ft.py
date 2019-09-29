import csv
import re
from datetime import datetime
from os import path
from typing import List, Optional

from beancount.core import amount, data
from beancount.core.data import Price
from beancount.core.number import D
from beancount.ingest.importer import ImporterProtocol

from importers.util import get_prices


def parse_iso8601(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')


def parse_dates(dates: List[str]) -> List[datetime]:
    return list(map(parse_iso8601, dates))


def find_series_by_type(series_type: str, series: List[dict]) -> Optional[dict]:
    return next((x for x in series if x['Type'] == series_type), None)


class FinancialTimesImporter(ImporterProtocol):
    """Importer for Financial Times market data."""

    def __init__(self, currency: str) -> None:
        self.currency = currency

    def name(self) -> str:
        return self.__class__.__name__

    __str__ = name

    def identify(self, file) -> bool:
        return path.basename(file.name).endswith('.price')

    def extract(self, file, existing_entries=None) -> List[Price]:
        commodity = re.sub(r'\.price$', '', path.basename(file.name))
        prices = []
        entry = 1

        with open(file.name) as csv_file:
            rows = csv.DictReader(csv_file, delimiter=',')

            for row in rows:
                label = row['Label']
                symbol = row['Symbol']

                response = get_prices(label, symbol)
                dates = parse_dates(response['Dates'])
                elements = response['Elements']

                for element in elements:
                    series = element['ComponentSeries']
                    close = find_series_by_type('Close', series)

                    if close is not None:
                        values = close['Values']

                        for idx, value in enumerate(values):
                            date = dates[idx]
                            price = '{0:.3f}'.format(value)
                            meta = data.new_metadata(file.name, entry)
                            prices.append(data.Price(meta, date, commodity, amount.Amount(D(price), self.currency)))
                            entry += 1

        return prices
