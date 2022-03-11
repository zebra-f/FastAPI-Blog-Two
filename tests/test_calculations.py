import pytest

from app.calculations import add, subtract, multiply, divide


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
