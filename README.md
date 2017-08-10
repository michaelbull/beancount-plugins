# beancount-importers

[![Build Status](https://travis-ci.org/michaelbull/beancount-importers.svg?branch=master)](https://travis-ci.org/michaelbull/beancount-importers)

A collection of my custom [beancount][beancount] importers, written in [Python 3.6+][python].

## LondonStockExchangeImporter

Import historic commodity price information from the London Stock Exchange.

`lse_config.py`:

```python
from src.importers.lse import LondonStockExchangeImporter

CONFIG = [
    LondonStockExchangeImporter('GBP')
]
```

**Output:**
```
$ cat prices/FTSE100.price
UKX.FTD

$ bean-extract lse_config.py prices/
;; -*- mode: beancount -*-
**** prices/FTSE100.price

2012-08-13 price FTSE100                            58.319 GBP

2012-08-14 price FTSE100                            58.648 GBP

2012-08-15 price FTSE100                            58.330 GBP

2012-08-16 price FTSE100                            58.345 GBP

2012-08-17 price FTSE100                            58.524 GBP

...

```

## PayslipImporter

Import a PDF payslip.

`payslip_config.py`:

```python
from src.importers.payslip import PayslipImporter

CONFIG = [
    PayslipImporter('Google', 'NatWest:Savings', 'GBP', student_loan=False)
]
```

**Output:**

```
$ tree payslips/
payslips/
└── june.pdf

$ bean-extract payslip_config.py payslips/
;; -*- mode: beancount -*-
**** payslips/june.pdf

2017-07-31 * "Google" "Salary"
  Expenses:Tax:Income               123.45 GBP
  Expenses:Tax:NationalInsurance    789.10 GBP
  Assets:NatWest:Savings           1122.33 GBP
  Income:Google:Salary    
```

## Developing

Create and activate a [`virtualenv`][virtualenv], then install the dependencies
using [pip][pip]:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements_dev.txt
```

## Testing

### Type Checker

[Mypy](mypy) is installed to run static type checking on the source files.

Run the following command to perform the static type analysis:

```
(venv)$ mypy --ignore-missing-imports .
```

### Unit Tests

Unit tests are written using [`pytest`][pytest].

Run the following command to execute the unit tests:

```
(venv)$ pytest -q
........
8 passed in 0.04 seconds
```

## Contributing

Bug reports and pull requests are welcome on [GitHub][github].

## License

This project is available under the terms of the ISC license. See the
[`LICENSE`](LICENSE) file for the copyright information and licensing terms.

[beancount]: http://furius.ca/beancount/
[python]: https://www.python.org/
[virtualenv]: https://virtualenv.pypa.io/en/stable/
[pip]: https://pypi.python.org/pypi/pip
[mpypy]: http://mypy-lang.org/
[pytest]: https://docs.pytest.org/en/latest/index.html
[github]: https://github.com/michaelbull/beancount-importers
