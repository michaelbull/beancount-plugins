import datetime
import re
from os import path
from typing import List

from beancount.core import amount, data
from beancount.core.data import Price
from beancount.core.number import D
from beancount.ingest.importer import ImporterProtocol

from .util import get_prices


class LondonStockExchangeImporter(ImporterProtocol):
    """Importer for London Stock Exchange commodity prices."""

    def __init__(self, currency: str) -> None:
        self.currency = currency

    def name(self) -> str:
        return self.__class__.__name__

    __str__ = name

    def identify(self, file) -> bool:
        return path.basename(file.name).endswith('.price')

    def extract(self, file) -> List[Price]:
        key = open(file.name).readline().splitlines()[0]
        commodity = re.sub('\.price$', '', path.basename(file.name))

        prices = []
        entry = 1
        response = get_prices(key)

        for d in response['d']:
            date = datetime.datetime.fromtimestamp(d[0] / 1000).date()
            price = '{0:.3f}'.format(d[1] / 100)
            meta = data.new_metadata(file.name, entry)
            prices.append(data.Price(meta, date, commodity, amount.Amount(D(price), self.currency)))
            entry += 1

        return prices
