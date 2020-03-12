def test_false():
    assert False

def test_True():
    assert True


def test_sum():
    assert 2+3 == 5


def test_division():
    assert 25/5 == 5


def test_string_properties():
    a = "Hello Folks!"
    assert len(a) == 12
    assert a[3:5] == 'lo'
    assert a.split(' ') == ['Hello', 'Folks!']

def test_dict():
    a = {
        "hello": "great"
    }

    assert a.get('hello') == 'great'
    assert a.get('UAU') is None

def test_list():
    a = [1,2,3,4,5,6]
    assert a[0] == 1
    assert a[-1] == 6


def test_concat():
    assert 'a' + 'b' == 'ab'