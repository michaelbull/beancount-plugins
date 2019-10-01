import datetime
import re
from typing import List

from beancount.core.amount import Amount
from beancount.core.data import EMPTY_SET, Posting, Transaction, new_metadata
from beancount.core.flags import FLAG_OKAY
from beancount.core.number import D
from beancount.ingest.cache import _FileMemo
from beancount.ingest.importer import ImporterProtocol

from .util import pdftotext


def find_date(payslip: str) -> datetime.date:
    date_pattern = re.compile(r'\d+/\d+/\d+')
    match = re.search(date_pattern, payslip)

    if match is None:
        raise Exception(f'No date match in {payslip}')
    else:
        return datetime.datetime.strptime(match.group(0), '%d/%m/%Y').date()


class PayslipImporter(ImporterProtocol):
    """Importer for payslips."""

    def __init__(self, employer: str, asset: str, currency: str, student_loan: bool) -> None:
        self.employer = employer
        self.asset = asset
        self.currency = currency
        self.student_loan = student_loan

    def identify(self, file: _FileMemo) -> bool:
        if file.mimetype() != 'application/pdf':
            return False
        else:
            payslip = file.convert(pdftotext)
            return True if payslip and 'Total Gross Pay' in payslip else False

    def extract(self, file: _FileMemo, existing_entries=None) -> List[Transaction]:
        payslip = file.convert(pdftotext)

        income_tax = Posting(
            account='Expenses:Tax:Income',
            units=self._find_amount('PAYE Tax', payslip),
            cost=None,
            price=None,
            flag=None,
            meta=None
        )

        national_insurance = Posting(
            account='Expenses:Tax:NationalInsurance',
            units=self._find_amount('National Insurance', payslip),
            cost=None,
            price=None,
            flag=None,
            meta=None
        )

        student_loan = Posting(
            account='Liabilities:StudentFinance',
            units=self._find_amount('Student Loan', payslip),
            cost=None,
            price=None,
            flag=None,
            meta=None
        ) if self.student_loan else None

        net_pay = Posting(
            account=f'Assets:{self.asset}',
            units=self._find_amount('Net Pay', payslip),
            cost=None,
            price=None,
            flag=None,
            meta=None
        )

        salary = Posting(
            account=f'Income:{self.employer}:Salary',
            units=None,
            cost=None,
            price=None,
            flag=None,
            meta=None
        )

        postings: List[Posting] = list(filter(None, [
            income_tax,
            national_insurance,
            student_loan,
            net_pay,
            salary
        ]))

        txn = Transaction(
            meta=new_metadata(file.name, int(1)),
            date=find_date(payslip),
            flag=FLAG_OKAY,
            payee=self.employer,
            narration='Salary',
            tags=EMPTY_SET,
            links=EMPTY_SET,
            postings=postings
        )

        return [txn]

    def file_account(self, file: _FileMemo) -> str:
        return f'Income:{self.employer}:Salary'

    def file_name(self, file: _FileMemo) -> str:
        return 'payslip.pdf'

    def file_date(self, file: _FileMemo) -> datetime.date:
        payslip = file.convert(pdftotext)
        return find_date(payslip)

    def _find_amount(self, qualifier: str, payslip: str) -> Amount:
        pattern = re.compile(qualifier + r'[ ]+(?P<amount>-?\d*\.?\d+)')
        match = re.search(pattern, payslip)

        if match is None:
            raise Exception(f'No amount in {payslip}')
        else:
            return Amount(D(match.group('amount')), self.currency)
