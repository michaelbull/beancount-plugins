import datetime
import re
from typing import List

from beancount.core import amount, data, flags
from beancount.core.amount import Amount
from beancount.core.data import Transaction
from beancount.core.number import D
from beancount.ingest.importer import ImporterProtocol

from .util import pdftotext


def find_date(payslip) -> datetime.date:
    date_pattern = re.compile('\d+/\d+/\d+')
    return datetime.datetime.strptime(re.search(date_pattern, payslip).group(0), '%d/%m/%Y').date()


class PayslipImporter(ImporterProtocol):
    """Importer for payslips."""

    def __init__(self, employer: str, asset: str, currency: str, student_loan: bool) -> None:
        self.employer = employer
        self.asset = asset
        self.currency = currency
        self.student_loan = student_loan

    def name(self) -> str:
        return self.__class__.__name__

    __str__ = name

    def identify(self, file) -> bool:
        if file.mimetype() != 'application/pdf':
            return False

        payslip = file.convert(pdftotext)
        return True if payslip and 'Total Gross Pay' in payslip else False

    def extract(self, file) -> List[Transaction]:
        payslip = file.convert(pdftotext)
        date = find_date(payslip)

        postings = []

        income_tax = self.find_amount('PAYE Tax', payslip)
        postings.append(data.Posting('Expenses:Tax:Income', income_tax, None, None, None, None))

        national_insurance = self.find_amount('National Insurance', payslip)
        postings.append(data.Posting('Expenses:Tax:NationalInsurance', national_insurance, None, None, None, None))

        if self.student_loan:
            student_loan = self.find_amount('Student Loan', payslip)
            postings.append(data.Posting('Liabilities:StudentFinance', student_loan, None, None, None, None))

        net_pay = self.find_amount('Net Pay', payslip)
        postings.append(data.Posting(f'Assets:{self.asset}', net_pay, None, None, None, None))

        postings.append(data.Posting(f'Income:{self.employer}:Salary', None, None, None, None, None))

        meta = data.new_metadata(file.name, int(1))
        txn = data.Transaction(meta, date, flags.FLAG_OKAY, self.employer, 'Salary', data.EMPTY_SET, data.EMPTY_SET,
                               postings)
        return [txn]

    def file_account(self, file) -> str:
        return f'Income:{self.employer}:Salary'

    def file_name(self, file) -> str:
        return 'payslip.pdf'

    def file_date(self, file) -> datetime.date:
        payslip = file.convert(pdftotext)
        return find_date(payslip)

    def find_amount(self, qualifier: str, payslip: str) -> Amount:
        pattern = re.compile(qualifier + '[ ]+(?P<amount>-?\d*\.?\d+)')
        return amount.Amount(D(re.search(pattern, payslip).group('amount')), self.currency)
