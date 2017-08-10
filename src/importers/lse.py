import datetime
import re
from os import path

from beancount.core import amount, data
from beancount.core.number import D

from src.util.lse import get_prices


class LondonStockExchangeImporter:
    """Importer for London Stock Exchange commodity prices."""

    def __init__(self, currency: str) -> None:
        self.currency = currency

    def name(self):
        """Return a unique id/name for this importer.

        Returns:
          A string which uniquely identifies this importer.
        """
        return self.__class__.__name__

    __str__ = name

    def identify(self, file):
        """Return true if this importer matches the given file.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          A boolean, true if this importer can handle this file.
        """
        return path.basename(file.name).endswith('.price')

    def extract(self, file):
        """Extract transactions from a file.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          A list of new, imported directives (usually mostly Transactions)
          extracted from the file.
        """
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
