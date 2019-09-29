# beancount-importers

[![Build Status](https://travis-ci.org/michaelbull/beancount-importers.svg?branch=master)](https://travis-ci.org/michaelbull/beancount-importers)

A collection of my custom [beancount][beancount] importers, written in [Python][python] (3.7).

## FinancialTimesImporter

Import historic commodity price information from the [Financial Times Funds][ft-funds].

### Usage

Add the following to `ft_config.py`:

```python
from importers.ft import FinancialTimesImporter

CONFIG = [
    FinancialTimesImporter('GBP')
]
```

Ensure you have a `.price` file in the `prices` directory, structured as a CSV
file with the fund's label and symbol. For example, the 
[`LU0011847091`](https://markets.ft.com/data/funds/tearsheet/summary?s=LU0011847091:GBP)
fund has the following label and symbol:

```
$ cat prices/LU0011847091.price
Label,Symbol
d9828b00,791
```

Run `bean-extract` to extract the prices:

```
$ bean-extract ft_config.py prices/
;; -*- mode: beancount -*-
**** prices/LU0011847091.price

2009-10-01 00:00:00 price LU0011847091                       51.470 GBP

2009-11-02 00:00:00 price LU0011847091                       52.810 GBP

2009-12-01 00:00:00 price LU0011847091                       54.650 GBP

2010-01-04 00:00:00 price LU0011847091                       53.230 GBP

2010-02-01 00:00:00 price LU0011847091                       54.790 GBP

2010-03-01 00:00:00 price LU0011847091                       58.900 GBP

...
```

## PayslipImporter

Import a PDF payslip.

### Usage

Add the following to `payslip_config.py`:

```python
from importers.payslip import PayslipImporter

CONFIG = [
    PayslipImporter('Google', 'NatWest:Savings', 'GBP', student_loan=False)
]
```

Ensure you have a payslip `.pdf` file in the `payslips` directory:

```
$ tree payslips/
payslips/
└── june.pdf
```

Run `bean-extract` to extract the transaction:

```
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
[ft-funds]: https://markets.ft.com/data/funds/uk
[virtualenv]: https://virtualenv.pypa.io/en/stable/
[pip]: https://pypi.python.org/pypi/pip
[mpypy]: http://mypy-lang.org/
[pytest]: https://docs.pytest.org/en/latest/index.html
[github]: https://github.com/michaelbull/beancount-importers
