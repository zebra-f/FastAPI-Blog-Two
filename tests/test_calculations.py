import pytest

from app.calculations import (add, subtract, multiply, divide, BankAccount,
                             InsufficientFundsException)


@pytest.fixture
def default_bank_account_fixture():
    return BankAccount()


@pytest.fixture
def bank_account_fixture():
    return BankAccount(100)   


@pytest.mark.parametrize("num1, num2, expected", [
    (15, 7, 22),
    (0, 2, 2),
    (-2, -2, -4),
    (-4, 1, -3)
])
def test_add(num1, num2, expected):
    print("testing addition")
    assert add(num1, num2) == expected
    
    assert add(3, 4) == 7
    assert add(1) == 3


def test_subtract():
    print("testing subtraction")
    assert subtract(3, 4) == -1
    assert subtract(1) == -1


def test_calculations():
    assert multiply(3, 4) == 12
    assert multiply(1) == 2

    assert divide(3, 4) == 3/4
    assert divide(1) == 0.5


def test_bank_account_one():
    
    customer_instance_one = BankAccount()
    assert customer_instance_one.balance == 0

    customer_instance_one.deposit(40)
    assert customer_instance_one.balance == 40

    customer_instance_one.withdraw(10)
    assert customer_instance_one.balance == 30


def test_bank_account_two():
    
    custom_instance_two = BankAccount(100)
    assert custom_instance_two.balance == 100

    custom_instance_two.deposit(40)
    assert custom_instance_two.balance == 140

    custom_instance_two.withdraw(10)
    assert custom_instance_two.balance == 130


def test_bank_defualt_balance(default_bank_account_fixture):
    assert default_bank_account_fixture.balance == 0


def test_bank_balance(bank_account_fixture):
    assert bank_account_fixture.balance == 100


def test_bank_withdraw(bank_account_fixture):
    bank_account_fixture.withdraw(10)
    assert bank_account_fixture.balance == 90


def test_bank_deposit(bank_account_fixture):
    bank_account_fixture.deposit(40)
    assert bank_account_fixture.balance == 140


@pytest.mark.parametrize("d, w, b", [
    (20, 10, 10),
    (1700, 0, 1700),
])
def test_bank_default(default_bank_account_fixture, d, w, b):
    default_bank_account_fixture.deposit(d)
    default_bank_account_fixture.withdraw(w)
    assert default_bank_account_fixture.balance == b


def test_bank_default_insufficient_funds(default_bank_account_fixture):
    with pytest.raises(InsufficientFundsException):
        default_bank_account_fixture.withdraw(40)
