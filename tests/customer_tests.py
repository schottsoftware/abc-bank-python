from nose.tools import assert_equals
from abcbank.account import Account, CHECKING, SAVINGS, MAXI_SAVINGS
from abcbank.customer import Customer


def test_statement():
    #statement test
    checkingAccount = Account(CHECKING)
    savingsAccount = Account(SAVINGS)
    henry = Customer("Henry").openAccount(checkingAccount)
    henry.openAccount(savingsAccount)
    checkingAccount.deposit(100.0)
    savingsAccount.deposit(4000.0)
    savingsAccount.withdraw(200.0)
    assert_equals(henry.getStatement(),
                  "Statement for Henry" +
                  "\n\nChecking Account\n  deposit $100.00\nTotal $100.00" +
                  "\n\nSavings Account\n  deposit $4000.00\n  withdrawal $200.00\nTotal $3800.00" +
                  "\n\nTotal In All Accounts $3900.00")
    
def test_transfer():
    #transfer test
    checkingAccount = Account(CHECKING)
    savingsAccount = Account(SAVINGS)
    andy = Customer("Andy").openAccount(checkingAccount)
    andy.openAccount(savingsAccount)
    savingsAccount.deposit(4000.0)
    savingsAccount.transfer(200.0,checkingAccount)
    assert_equals(andy.getStatement(),
                  "Statement for Andy" +
                  "\n\nChecking Account\n  deposit $200.00\nTotal $200.00" +
                  "\n\nSavings Account\n  deposit $4000.00\n  withdrawal $200.00\nTotal $3800.00" +
                  "\n\nTotal In All Accounts $4000.00")

def test_oneAccount():
    #single account test
    oscar = Customer("Oscar").openAccount(Account(SAVINGS))
    assert_equals(oscar.numAccs(), 1)


def test_twoAccounts():
    #two account test
    jerry = Customer("Jerry").openAccount(Account(SAVINGS))
    jerry.openAccount(Account(CHECKING))
    assert_equals(jerry.numAccs(), 2)


def test_threeAccounts():
    #two account test
    steve = Customer("Steve").openAccount(Account(SAVINGS))
    steve.openAccount(Account(CHECKING))
    steve.openAccount(Account(MAXI_SAVINGS))
    assert_equals(steve.numAccs(), 3)
    
    
    