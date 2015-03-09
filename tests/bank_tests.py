from nose.tools import assert_equals
from abcbank.account import Account, CHECKING, MAXI_SAVINGS, SAVINGS
from abcbank.bank import Bank
from abcbank.customer import Customer


def test_customer_summary():
    bank = Bank()
    john = Customer("John").openAccount(Account(CHECKING))
    bank.addCustomer(john)
    assert_equals(bank.customerSummary(),
                  "Customer Summary\n - John (1 account)")


def test_checking_account():
    bank = Bank()
    checkingAccount = Account(CHECKING)
    bill = Customer("Bill").openAccount(checkingAccount)
    bank.addCustomer(bill)
    checkingAccount.deposit(100.0)
    assert_equals(bank.totalInterestPaid(), 0.1)


def test_savings_account():
    bank = Bank()
    checkingAccount = Account(SAVINGS)
    bank.addCustomer(Customer("Andrew").openAccount(checkingAccount))
    checkingAccount.deposit(1500.0)
    assert_equals(bank.totalInterestPaid(), 2.0)


def test_maxi_savings_account():
    bank = Bank()
    checkingAccount = Account(MAXI_SAVINGS)
    bank.addCustomer(Customer("Gabriela").openAccount(checkingAccount))
    checkingAccount.deposit(3000.0)
    assert_equals(bank.totalInterestPaid(), 176.62)