# PyTest checkup


def add(num1: int, num2: int=2) -> int:
    return num1 + num2


def subtract(num1: int, num2: int=2) -> int:
    return num1 - num2


def multiply(num1: int, num2: int=2) -> int:
    return num1 * num2


def divide(num1: int, num2: int=2) -> int:
    return num1 / num2


class InsufficientFundsException(Exception):
    pass


class BankAccount:
    
    def __init__(self, balance=0):
        self.balance = balance

    
    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsException("Insufficient funds!")
        
        self.balance -= amount


    def deposit(self, amount):
        self.balance += amount

