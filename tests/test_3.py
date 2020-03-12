class TestCase():
    @classmethod
    def setup_class(cls):
        cls.a = 123
        cls.b = 125

    def test_a_plus_b(self):
        assert self.a + self.b == 248

    def test_a_minus_b(self):
        assert self.a - self.b == -3

    def test_b_minus_a(self):
        assert self.b - self.a == 3

    def test_a_times_b(self):
        assert self.a * self.b != 1598