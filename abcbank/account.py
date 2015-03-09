from abcbank.transaction import Transaction
import json, os
CHECKING = 0
SAVINGS = 1
MAXI_SAVINGS = 2

full_path = os.path.realpath(__file__) 
config = os.path.dirname(full_path) + "/config.json"

class Account(object):
    def __init__(self, accountType):
        self.accountType = accountType
        self.configPath = ""
        self.transactions = []

    def deposit(self, amount):
        #deposits an amount into a customer's account
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.transactions.append(Transaction(amount))

    def withdraw(self, amount):
        #withdraws the amount specified from the customer's account
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.transactions.append(Transaction(-amount))
            
    def transfer(self, amount, toAcct):
        #transfers the amount specified from one account to another. 
        #Once hooked into a database we can set a max for transfers based on account balances.
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.transactions.append(Transaction(-amount))
            toAcct.transactions.append(Transaction(amount))
        

    def interestEarned(self, duration=None):
        #interest eared over a duration, duration is expressed as 1 being one year,
        #This version utilizes a json config file so that it can be quickly referenced
        #by many files and easily edited without effecting the rest of the system or
        #requiring a recommit.
        json_data = open(config)
        data = json.load(json_data)
        json_data.close()
        amount = self.sumTransactions()
        #these allow for the use of duration and compound frequency without being required.
        if duration is None:
            duration = 1

        if self.accountType == SAVINGS:
            sb1=data["savings"][0]["breakpoint"]
            sr1=data["savings"][0]["rate"]
            sr2=data["savings"][1]["rate"]
            sf =data["savings"][0]["frequency"]
            freq = sf
            if (amount <= sb1):
                rate = sr1
                earned =  self.interestEarnedTime(amount,rate,freq,duration)
                self.result = self.twoPlaces(earned)
            else:
                rate = sr2
                sofar = self.interestEarnedTime(sb1,sr1,freq,duration)
                sb2 = self.interestEarnedTime((amount-sb1),rate,freq,duration)
                earned = sofar + sb2
                self.result = self.twoPlaces(earned)

        elif self.accountType == MAXI_SAVINGS:
            mb1=data["maxi"][0]["breakpoint"]
            mr1=data["maxi"][0]["rate"]
            mb2=data["maxi"][1]["breakpoint"]
            mr2=data["maxi"][1]["rate"]
            mr3=data["maxi"][2]["rate"]
            mf =data["maxi"][0]["frequency"]
            freq = mf
            if (amount <= mb1):
                rate = mr1
                earned =  self.interestEarnedTime(amount,rate,freq,duration)
                self.result = self.twoPlaces(earned)

            elif (amount <= mb2):
                rate = mr2
                principal = amount - mb1
                earned =(mr1*mb1) + self.interestEarnedTime(principal,rate,freq,duration)
                self.result = self.twoPlaces(earned)

            else:
                rate = mr3
                principal = amount - mb2
                c1 = self.interestEarnedTime(mb1,mr1,freq,duration)
                c2 = self.interestEarnedTime((mb2-mb1),mr2,freq,duration)
                res = self.interestEarnedTime(principal,rate,freq,duration)
                earned =  c1 + c2 + res
                self.result = self.twoPlaces(earned)

        elif self.accountType == CHECKING:
            cr1=data["checking"][0]["rate"]
            cf =data["checking"][0]["frequency"]
            freq = cf
            rate = cr1 
            earned = self.interestEarnedTime(amount,rate,freq,duration)
            self.result = self.twoPlaces(earned)

        return self.result

    def sumTransactions(self, checkAllTransactions=True):
        return sum([t.amount for t in self.transactions])
    
    def twoPlaces(self,value):
        #quick reusable funciton to round to 2 spots to make it easier to put in to a dollar value 
        return float("{0:.2f}".format(value))
        
    def interestEarnedTime(self,principal, rate,times_per_year, years):
        #this function is the formula for interest and it can be set up to account 
        #for duration as well as compound frequency
        # (1 + r/n)
        body = 1 + (rate / times_per_year)
        # nt
        exponent = times_per_year * years
        # P(1 + r/n)^nt
        return principal * pow(body, exponent) -principal

