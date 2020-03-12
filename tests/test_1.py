import math

def sum(a, b):
    return a + b


def test_my_function():
    for i in range(30000):
        assert True


def test_failing_test():
    assert not 1 == 2


def test_sum():
    assert sum('a', 'b') == 'ab'
    assert sum(3, 2) == 5
    assert sum(2.9, 3) == 5.9


def test_trigonometry():
    assert math.cos(2*math.pi) != 1


def test_pouer():
    assert math.pow(2, 3) == 8


def test_float_sum():
    assert 2.5 + 3.9 == 6.4


def test_all():
    pass
