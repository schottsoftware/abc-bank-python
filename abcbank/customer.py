from abcbank.account import CHECKING, SAVINGS, MAXI_SAVINGS


class Customer:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def openAccount(self, account):
        #opens an account for customer
        self.accounts.append(account)
        return self

    def numAccs(self):
        #this returns the number of accounts
        return len(self.accounts)

    def totalInterestEarned(self):
        #Returns the total interest earned across all acounts
        return sum([a.interestEarned() for a in self.accounts])
    
    def getStatement(self):
    # This method gets a statement
        totalAcrossAllAccounts = sum([a.sumTransactions() for a in self.accounts])
        statement = "Statement for %s" % self.name
        for account in self.accounts:
            statement = statement + self.statementForAccount(account)
        statement = statement + "\n\nTotal In All Accounts " + _toDollars(totalAcrossAllAccounts)
        return statement

    def statementForAccount(self, account):
        # This puts the statement in a human readable format.
        accountType = "\n\n\n"
        if account.accountType == CHECKING:
            accountType = "\n\nChecking Account\n"
        if account.accountType == SAVINGS:
            accountType = "\n\nSavings Account\n"
        if account.accountType == MAXI_SAVINGS:
            accountType = "\n\nMaxi Savings Account\n"
        transactionSummary = [self.withdrawalOrDepositText(t) + " " + _toDollars(abs(t.amount))
                              for t in account.transactions]
        joinedTransactionSummary = "  " + "\n  ".join(transactionSummary) + "\n"
        self.balance = sum([t.amount for t in account.transactions])
        totalSummary = "Total " + _toDollars(self.balance)
        return accountType + joinedTransactionSummary + totalSummary

    def withdrawalOrDepositText(self, transaction):
        #returns proper text for if a transaction was a withdrawal or deposit 
        if transaction.amount < 0:
            return "withdrawal"
        elif transaction.amount > 0:
            return "deposit"
        else:
            return "N/A"


def _toDollars(number):
    #returns float value to dollars. 
    return "${:1.2f}".format(number)
