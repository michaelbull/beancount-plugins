#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
from typing import List, Pattern

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


def pattern_for(field_name: str) -> Pattern[str]:
    return re.compile(field_name + '[ ]+(-?\d*\.?\d+)')


def find(pattern: Pattern[str], text: str) -> str:
    match = re.search(pattern, text)
    if match:
        return match.group(1)
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

    date = find(re.compile('(\d+/\d+/\d+)'), content)
    income_tax = find(pattern_for('PAYE Tax'), content)
    national_insurance = find(pattern_for('National Insurance'), content)

    transaction += [
        date + ' * "' + employer + '"',
        '  Expenses:Tax:Income ' + income_tax + ' ' + currency,
        '  Expenses:Tax:NationalInsurance ' + national_insurance + ' ' + currency,
    ]

    if student_loan:
        repayment = find(pattern_for('Student Loan'), content)
        transaction += ['  Liabilities:StudentFinance ' + repayment + ' ' + currency]

    net_pay = find(pattern_for('Net Pay'), content)
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
