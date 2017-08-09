import re

from parse_payslip import build_transaction, find, pattern_for


def test_pattern_for_field() -> None:
    pattern = pattern_for('example')
    match = re.search(pattern, 'example       5145.05')
    assert match.group(1) == '5145.05'


def test_pattern_for_mismatch():
    pattern = pattern_for('my pattern')
    match = re.search(pattern, 'this is wrong')
    assert match is None


def test_find_group() -> None:
    pattern = re.compile('(\d+)')
    match = find(pattern, '505')
    assert match == '505'


def test_find_mismatch() -> None:
    pattern = re.compile('(\d+)')
    match = find(pattern, 'not a number')
    assert match == ''


def test_build_transaction() -> None:
    content = '''
        Date                    2017/10/05
        PAYE Tax                5050.10
        National Insurance      7891.30
        Student Loan            1033.41
        Net Pay                 18533.87
    '''

    transaction = build_transaction(content, 'GBP', 'Google', 'NatWest:Current', True)

    assert transaction == [
        '2017/10/05 * "Google"',
        '  Expenses:Tax:Income 5050.10 GBP',
        '  Expenses:Tax:NationalInsurance 7891.30 GBP',
        '  Liabilities:StudentFinance 1033.41 GBP',
        '  Assets:NatWest:Current 18533.87 GBP',
        '  Income:Google:Salary'
    ]
