from app.calculations import add


def test_add():
    print("testing function")
    assert add(3, 4) == 7

test_add()

