import unittest
from converter import Converter


class TestConverter(unittest.TestCase):

    # ============================================================
    # 1. x >= 100.7 → 1000
    # ============================================================
    def test_upper_range_regular(self):
        self.assertEqual(Converter.do(150.5), 1000)

    def test_upper_range_boundary(self):
        # Граница включена: 100.7 → 1000
        self.assertEqual(Converter.do(100.7), 1000)

    def test_upper_range_large(self):
        self.assertEqual(Converter.do(1_000_000.0), 1000)

    # ============================================================
    # 2. 0 < x < 100.7 → int(x)
    # ============================================================
    def test_middle_range_regular(self):
        self.assertEqual(Converter.do(65.7), 65)
        self.assertEqual(Converter.do(0.9), 0)

    def test_middle_range_boundary_near_upper(self):
        # 100.6 — ближайшее к 100.7 снизу с точностью 0.1
        self.assertEqual(Converter.do(100.6), 100)

    def test_middle_range_boundary_near_zero(self):
        # 0.1 — ближайшее к 0 сверху
        self.assertEqual(Converter.do(0.1), 0)

    # ============================================================
    # 3. x == 0.0 → ValueError
    # ============================================================
    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    # ============================================================
    # 4. -30.4 <= x < 0 → int(x) - 5
    # ============================================================
    def test_lower_middle_regular(self):
        self.assertEqual(Converter.do(-0.1), -5)     # int(-0.1)=-0=0 → -5
        self.assertEqual(Converter.do(-10.5), -15)   # int(-10.5)=-10 → -15

    def test_lower_middle_boundary(self):
        # -30.4 — граница включена
        self.assertEqual(Converter.do(-30.4), -35)   # int(-30.4)=-30 → -35

    # ============================================================
    # 5. x <= -30.5 → -2000
    # ============================================================
    def test_bottom_range_boundary(self):
        # -30.5 — граница включена
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_bottom_range_regular(self):
        self.assertEqual(Converter.do(-94.5), -2000)
        self.assertEqual(Converter.do(-1000.0), -2000)


if __name__ == "__main__":
    unittest.main()