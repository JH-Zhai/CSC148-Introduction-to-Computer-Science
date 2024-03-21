"""CSC148 Prep 3: Inheritance

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Prep 3.

WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
Add your own to practice writing tests and to be confident your code is correct.
You must write at least 2 additional test cases.
"""
from datetime import date

from prep3 import SalariedEmployee, HourlyEmployee, Company


def test_total_pay_basic() -> None:
    e = SalariedEmployee(14, 'Gilbert the cat', 1200.0)
    e.pay(date(2018, 6, 28))
    e.pay(date(2018, 7, 28))
    e.pay(date(2018, 8, 28))
    assert e.total_pay() == 300.0

    e = SalariedEmployee(14, 'Gilbert the cat', 2400.0)
    e.pay(date(2018, 6, 28))
    e.pay(date(2018, 7, 28))
    e.pay(date(2018, 8, 28))
    assert e.total_pay() == 600.0


def test_total_payroll_mixed() -> None:
    my_corp = Company([SalariedEmployee(24, 'Gilbert the cat', 1200.0),
                       HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)])
    my_corp.pay_all(date(2018, 6, 28))
    assert my_corp.total_payroll() == 600.25

    my_corp2 = Company([])
    my_corp2.pay_all(date(2018, 6, 24))
    assert my_corp2.total_payroll() == 0


if __name__ == '__main__':
    import pytest

    pytest.main(['prep3_sample_test.py'])
