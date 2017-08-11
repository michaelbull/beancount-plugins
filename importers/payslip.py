import datetime
import re
from decimal import Decimal

from beancount.core import amount, data, flags
from beancount.core.number import D

from importers.util import pdftotext


def find_date(payslip):
    date_pattern = re.compile('\d+/\d+/\d+')
    return datetime.datetime.strptime(re.search(date_pattern, payslip).group(0), '%d/%m/%Y').date()


class PayslipImporter:
    """Importer for payslips."""

    def __init__(self, employer: str, asset: str, currency: str, student_loan: bool) -> None:
        self.employer = employer
        self.asset = asset
        self.currency = currency
        self.student_loan = student_loan

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
        if file.mimetype() != 'application/pdf':
            return False

        payslip = file.convert(pdftotext)
        return True if payslip and 'Total Gross Pay' in payslip else False

    def extract(self, file):
        """Extract transactions from a file.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          A list of new, imported directives (usually mostly Transactions)
          extracted from the file.
        """
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

    def file_account(self, file):
        """Return an account associated with the given file.

        Note: If you don't implement this method you won't be able to move the
        files into its preservation hierarchy; the bean-file command won't work.

        Also, normally the returned account is not a function of the input
        file--just of the importer--but it is provided anyhow.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          The name of the account that corresponds to this importer.
        """
        return f'Income:{self.employer}:Salary'

    def file_name(self, file):
        """A filter that optionally renames a file before filing.

        This is used to make tidy filenames for filed/stored document files. The
        default implementation just returns the same filename. Note that a
        simple RELATIVE filename must be returned, not an absolute filename.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          The tidied up, new filename to store it as.
        """
        return 'payslip.pdf'

    def file_date(self, file):
        """Attempt to obtain a date that corresponds to the given file.

        Args:
          file: A cache.FileMemo instance.
        Returns:
          A date object, if successful, or None if a date could not be extracted.
          (If no date is returned, the file creation time is used. This is the
          default.)
        """
        payslip = file.convert(pdftotext)
        return find_date(payslip)

    def find_amount(self, qualifier: str, payslip: str) -> Decimal:
        pattern = re.compile(qualifier + '[ ]+(?P<amount>-?\d*\.?\d+)')
        return amount.Amount(D(re.search(pattern, payslip).group('amount')), self.currency)
