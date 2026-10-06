import unittest
import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from triangle import process_triangle, _parse_side, _is_triangle, _triangle_type, FIELD_SIZE, MARGIN


class TestParseSide(unittest.TestCase):
    """Тесты парсинга стороны"""

    def test_parse_side_accepts_integer_string(self):
        self.assertEqual(_parse_side("5"), 5.0)

    def test_parse_side_accepts_float_string(self):
        self.assertEqual(_parse_side("3.5"), 3.5)

    def test_parse_side_raises_error_for_non_numeric_string(self):
        with self.assertRaises(ValueError):
            _parse_side("abc")

    def test_parse_side_raises_error_for_empty_string(self):
        with self.assertRaises(ValueError):
            _parse_side("")

    def test_parse_side_raises_error_for_zero(self):
        with self.assertRaises(ValueError):
            _parse_side("0")

    def test_parse_side_raises_error_for_negative_number(self):
        with self.assertRaises(ValueError):
            _parse_side("-3")

    def test_parse_side_raises_error_for_nan(self):
        with self.assertRaises(ValueError):
            _parse_side("nan")

    def test_parse_side_raises_error_for_infinity(self):
        with self.assertRaises(ValueError):
            _parse_side("inf")


class TestIsTriangle(unittest.TestCase):
    """Тесты неравенства треугольника"""

    def test_is_triangle_true_for_equilateral(self):
        self.assertTrue(_is_triangle(3, 3, 3))

    def test_is_triangle_true_for_classic_345(self):
        self.assertTrue(_is_triangle(3, 4, 5))

    def test_is_triangle_false_when_sum_equals_third_side(self):
        # Вырожденный случай: 1+2=3 — не треугольник
        self.assertFalse(_is_triangle(1, 2, 3))

    def test_is_triangle_false_when_one_side_too_long(self):
        self.assertFalse(_is_triangle(1, 2, 10))


class TestTriangleType(unittest.TestCase):
    """Тесты определения типа"""

    def test_triangle_type_equilateral(self):
        self.assertEqual(_triangle_type(3, 3, 3), "равносторонний")

    def test_triangle_type_isosceles(self):
        self.assertEqual(_triangle_type(5, 5, 8), "равнобедренный")

    def test_triangle_type_scalene(self):
        self.assertEqual(_triangle_type(3, 4, 5), "разносторонний")

    def test_triangle_type_not_a_triangle(self):
        self.assertEqual(_triangle_type(1, 2, 10), "не треугольник")


class TestProcessTriangle(unittest.TestCase):
    """Тесты основной функции process_triangle"""

    def test_process_triangle_returns_equilateral_type(self):
        t_type, _ = process_triangle("3", "3", "3")
        self.assertEqual(t_type, "равносторонний")

    def test_process_triangle_returns_isosceles_type(self):
        t_type, _ = process_triangle("5", "5", "8")
        self.assertEqual(t_type, "равнобедренный")

    def test_process_triangle_returns_scalene_type(self):
        t_type, _ = process_triangle("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")

    def test_process_triangle_returns_not_a_triangle(self):
        t_type, _ = process_triangle("1", "2", "10")
        self.assertEqual(t_type, "не треугольник")

    def test_process_triangle_returns_empty_type_on_invalid_input(self):
        t_type, vertices = process_triangle("abc", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(vertices, [(-2, -2), (-2, -2), (-2, -2)])

    def test_process_triangle_returns_sentinel_for_not_a_triangle(self):
        _, vertices = process_triangle("1", "2", "10")
        self.assertEqual(vertices, [(-1, -1), (-1, -1), (-1, -1)])

    def test_process_triangle_returns_three_vertices(self):
        _, vertices = process_triangle("3", "4", "5")
        self.assertEqual(len(vertices), 3)

    def test_process_triangle_vertices_are_integers(self):
        _, vertices = process_triangle("3", "4", "5")
        for x, y in vertices:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_process_triangle_vertices_inside_field(self):
        _, vertices = process_triangle("3", "4", "5")
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, FIELD_SIZE)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, FIELD_SIZE)

    def test_process_triangle_accepts_float_strings(self):
        t_type, _ = process_triangle("3.5", "4.5", "5.5")
        self.assertEqual(t_type, "разносторонний")

    def test_process_triangle_zero_side_returns_error_sentinel(self):
        t_type, vertices = process_triangle("0", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(vertices, [(-2, -2), (-2, -2), (-2, -2)])

    def test_process_triangle_negative_side_returns_error_sentinel(self):
        t_type, _ = process_triangle("-3", "4", "5")
        self.assertEqual(t_type, "")


if __name__ == "__main__":
    unittest.main()