class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def display_info(self):
        print(f"Account Owner: {self.owner}")
        print(f"Balance: {self.balance}")

class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)  # Call parent constructor
        self.interest_rate = interest_rate

    # Overriding the display_info method
    def display_info(self):
        super().display_info()  # Optionally call the base version
        print(f"Interest Rate: {self.interest_rate}%")

# Usage
acc = SavingsAccount("Alice", 10000, 3.5)
acc.display_info()
