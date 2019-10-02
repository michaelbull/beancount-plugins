# beancount-plugins

[![Build Status](https://travis-ci.org/michaelbull/beancount-plugins.svg?branch=master)](https://travis-ci.org/michaelbull/beancount-plugins)

A collection of my custom [beancount][beancount] importers & price sources, written in [Python][python] (3.7).

## payslip.Importer

Import a PDF payslip.

### Usage

Add the following to `payslip_config.py`:

```python
from importers import payslip

CONFIG = [
    payslip.Importer('Google', 'NatWest:Savings', 'GBP', student_loan=False)
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
(venv)$ PYTHONPATH=. bean-extract ft_config.py prices/
```

## Type Checking

[Mypy](mypy) is installed to run static type checking on the source files.

Run the following command to perform the static type analysis:

```
(venv)$ mypy --ignore-missing-imports .
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
[github]: https://github.com/michaelbull/beancount-plugins
