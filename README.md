# beancount-parsers

[![Build Status](https://travis-ci.org/michaelbull/beancount-parsers.svg?branch=master)](https://travis-ci.org/michaelbull/beancount-parsers)

A collection of [Python 3.6+][python] scripts to parse a variety of data sources
into a [beancount][beancount] journal.

## Parsers

### `parse_lse.py`

Parse historic commodity price information from the London Stock Exchange.

New price information is appended to the specified beancount journal.

#### Example

```
$ ./parse_lse.py UKX.FTD FTSE100 FTSE100.beancount
Wrote 1262 new price(s).

$ head -5 FTSE100.beancount
2012-08-09 price FTSE100 58.515 GBP
2012-08-10 price FTSE100 58.471 GBP
2012-08-13 price FTSE100 58.319 GBP
2012-08-14 price FTSE100 58.648 GBP
2012-08-15 price FTSE100 58.330 GBP
```

### `parse_payslip.py`

Parse a payslip in PDF format and append it to a beancount journal as a new
transaction.

#### Example

```
$ ./parse_payslip.py payslip.pdf journal.beancount
Saved transaction to journal.beancount

$ tail -5 journal.beancount
31/07/2017 * "Work"
  Expenses:Tax:Income 1234.56 GBP
  Expenses:Tax:NationalInsurance 789.10 GBP
  Assets:Bank 1122.33 GBP
  Income:Work:Salary
```

## Developing

Create and activate a [`virtualenv`][virtualenv], then install the dependencies
using [pip][pip]:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements_frozen.txt
```

## Testing

### Type Checker

[Mypy](mypy) is installed to run static type checking on the source files.

Run the following command to perform the static type analysis:

```
(venv)$ mypy .
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

[python]: https://www.python.org/
[beancount]: http://furius.ca/beancount/
[virtualenv]: https://virtualenv.pypa.io/en/stable/
[pip]: https://pypi.python.org/pypi/pip
[mpypy]: http://mypy-lang.org/
[pytest]: https://docs.pytest.org/en/latest/index.html
[github]: https://github.com/michaelbull/beancount-parsers
