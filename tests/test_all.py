import unittest
from unittest.mock import Mock, patch

from calculator import TriangleCalculator
from database import TriangleDB
from user_io import UserIO, ConsoleUserIO
from notifier import Notifier
from controller import Controller


# ============================================================
# ЮНИТ-ТЕСТЫ (2 шт.) — проверяют один модуль в изоляции
# ============================================================

class TestCalculatorUnit(unittest.TestCase):
    def test_calculator_equilateral(self):
        calc = TriangleCalculator()
        ttype, err = calc.calculate("3", "3", "3")
        self.assertEqual(ttype, "равносторонний")
        self.assertIsNone(err)

    def test_calculator_invalid_triangle(self):
        calc = TriangleCalculator()
        ttype, err = calc.calculate("1", "2", "10")
        self.assertIsNone(ttype)
        self.assertIn("не образуют", err)


class TestDatabaseUnit(unittest.TestCase):
    def test_db_add_get_delete(self):
        db = TriangleDB()
        db.add(3, 3, 3, "равносторонний", None)
        self.assertEqual(db.get(3, 3, 3), ("равносторонний", None))
        db.delete(3, 3, 3)
        self.assertIsNone(db.get(3, 3, 3))


# ============================================================
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ (3 шт.)
# Проверяют совместную работу Controller + Calculator + DB + Notifier
# ============================================================

class TestControllerIntegration(unittest.TestCase):
    def test_full_flow_new_data(self):
        """Данных нет в БД → считаем, сохраняем, отправляем."""
        user_io = Mock(spec=UserIO)
        user_io.get_input.return_value = ("3", "3", "3")

        notifier = Mock(spec=Notifier)
        notifier.send.return_value = True

        ctrl = Controller(user_io, TriangleDB(), notifier, TriangleCalculator())
        res = ctrl.run()

        self.assertIn("равносторонний", res["result"])
        self.assertEqual(res["source"], "вычисления")
        notifier.send.assert_called_once()

    def test_full_flow_from_db(self):
        """Данные уже в БД → берём оттуда, не считаем."""
        db = TriangleDB()
        db.add(3.0, 3.0, 3.0, "равносторонний", None)

        user_io = Mock(spec=UserIO)
        user_io.get_input.return_value = ("3", "3", "3")

        notifier = Mock(spec=Notifier)

        ctrl = Controller(user_io, db, notifier, TriangleCalculator())
        res = ctrl.run()

        self.assertEqual(res["source"], "БД")
        notifier.send.assert_called_once()

    def test_full_flow_error_saved_to_db(self):
        """Ошибка валидации: сохраняется в БД и уходит в notifier."""
        db = TriangleDB()
        user_io = Mock(spec=UserIO)
        user_io.get_input.return_value = ("1", "2", "10")

        notifier = Mock(spec=Notifier)

        ctrl = Controller(user_io, db, notifier, TriangleCalculator())
        res = ctrl.run()

        self.assertIn("Ошибка", res["result"])
        self.assertIsNotNone(db.get(1.0, 2.0, 10.0))
        notifier.send.assert_called_once()


# ============================================================
# ТЕСТЫ ИЗОЛЯЦИИ С ЗАГЛУШКАМИ (2 шт.)
# ============================================================

class TestUserIOIsolation(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", "3", "3"])
    def test_console_input(self, mock_input):
        """Проверяем ConsoleUserIO, подменив input()."""
        io = ConsoleUserIO()
        self.assertEqual(io.get_input(), ("3", "3", "3"))
        self.assertEqual(mock_input.call_count, 3)


class TestNotifierIsolation(unittest.TestCase):
    def test_notifier_mock(self):
        """Имитация внешнего сервера через Mock."""
        n = Mock(spec=Notifier)
        n.send.return_value = True
        self.assertTrue(n.send("msg"))
        n.send.assert_called_once_with("msg")


if __name__ == "__main__":
    unittest.main()