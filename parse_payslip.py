#!/usr/bin/env python3

import argparse
import subprocess
import sys
from typing import List, Pattern

import re

Transaction = List[str]


def parse_args():
    parser = argparse.ArgumentParser(
        description='Parse a payslip in PDF format and append it to a beancount file as a new transaction.'
    )
    parser.add_argument('pdf_file',
                        help='The input PDF file to parse, e.g. payslip.pdf')
    parser.add_argument('beancount_file',
                        help='The beancount file to write to, e.g. ledger.beancount')
    parser.add_argument('-a', '--asset', default='Bank',
                        help='Specifies the asset to which the net pay should be allocated. Defaults to Bank.')
    parser.add_argument('-c', '--currency', default='GBP',
                        help='Specifies the currency to use. Defaults to GBP.')
    parser.add_argument('-e', '--employer', default='Work',
                        help='Specifies name of the employer. Defaults to Work.')
    parser.add_argument('-s', '--student_loan', action='store_true',
                        help='Include Student Loan repayment information.')
    return parser.parse_args()


def field_pattern(field_name: str) -> Pattern[str]:
    return re.compile(field_name + '[ ]+(?P<field>-?\d*\.?\d+)')


def find(pattern: Pattern[str], group: str, text: str) -> str:
    match = re.search(pattern, text)
    if match:
        return match.group(group)
    else:
        return ''


def append_transaction(file: str, lines: List[str]) -> None:
    with open(file, 'a') as out:
        out.write('\n'.join(['', *lines, '']))
    print('Saved transaction to ' + file)


def pdftotext(file: str) -> str:
    try:
        return subprocess.check_output(['pdftotext', '-layout', file, '-']).decode('utf-8')
    except subprocess.CalledProcessError as e:
        sys.exit('Error running pdftotext: ' + e.output)


def build_transaction(content: str, currency: str, employer: str, asset: str, student_loan: bool) -> Transaction:
    transaction: Transaction = []

    date = find(re.compile('(?P<date>\d+/\d+/\d+)'), 'date', content)
    income_tax = find(field_pattern('PAYE Tax'), 'field', content)
    national_insurance = find(field_pattern('National Insurance'), 'field', content)
    net_pay = find(field_pattern('Net Pay'), 'field', content)

    transaction += [
        date + ' * "' + employer + '"',
        '  Expenses:Tax:Income ' + income_tax + ' ' + currency,
        '  Expenses:Tax:NationalInsurance ' + national_insurance + ' ' + currency,
    ]

    if student_loan:
        repayment = find(field_pattern('Student Loan'), 'field', content)
        transaction += ['  Liabilities:StudentFinance ' + repayment + ' ' + currency]

    transaction += [
        '  Assets:' + asset + ' ' + net_pay + ' ' + currency,
        '  Income:' + employer + ':Salary'
    ]

    return transaction


def main() -> None:
    args = parse_args()
    content = pdftotext(args.pdf_file)

    if content == '':
        sys.exit('Failed to read text content from PDF file.')
    else:
        transaction = build_transaction(content, args.currency, args.employer, args.asset, args.student_loan)
        append_transaction(args.beancount_file, transaction)


if __name__ == '__main__':
    main()
