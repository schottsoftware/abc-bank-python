class Bank:
    def __init__(self):
        self.customers = []

    def addCustomer(self, customer):
        self.customers.append(customer)
        
    def customerSummary(self):
        #returns a summary of a customer's accounts
        summary = "Customer Summary"
        for customer in self.customers:
            summary = summary + "\n - " + customer.name + " (" + self._format(customer.numAccs(), "account") + ")"
        return summary
    
    def _format(self, number, word):
        #returns a formatted string with the proper sytax
        return str(number) + " " + (word if (number == 1) else word + "s")
    
    def totalInterestPaid(self):
        #returns the total interest paid by the bank to all customers requested 
        total = 0
        for c in self.customers:
            total += c.totalInterestEarned()
        return total
    
    def getFirstCustomer(self):
        #returns the first cutomer's name
        try:
            self.customers = None
            return self.customers[0].name
        except Exception as e:
            print(e)
            return "Error"