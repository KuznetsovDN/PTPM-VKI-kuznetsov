import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Delivery import calculate_delivery_cost


class TestDeliveryValidation(unittest.TestCase):
    """Тесты валидации входных данных"""

    def test_negative_weight_returns_error(self):
        cost, date = calculate_delivery_cost(-1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_zero_weight_returns_error(self):
        cost, _ = calculate_delivery_cost(0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_too_light_returns_error(self):
        cost, _ = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_over_50_returns_error(self):
        cost, _ = calculate_delivery_cost(51, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_zero_distance_returns_error(self):
        cost, _ = calculate_delivery_cost(5, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_over_5000_returns_error(self):
        cost, _ = calculate_delivery_cost(5, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_package_type_returns_error(self):
        cost, _ = calculate_delivery_cost(5, 100, "неизвестный")
        self.assertEqual(cost, -1)


class TestDeliveryCostCalculation(unittest.TestCase):
    """Тесты расчёта стоимости"""

    def test_base_cost_for_light_parcel(self):
        """Вес <= 5 кг — без надбавки: 200 + 100*5 = 700"""
        cost, _ = calculate_delivery_cost(3, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_surcharge_20_percent(self):
        """🐛 БАГ: вес ровно 5.0 не попадает ни в одну ветку надбавки"""
        cost, _ = calculate_delivery_cost(10, 100, "обычный")
        # ожидаем 700 * 1.2 = 840
        self.assertEqual(cost, 840)

    def test_weight_just_above_5_gets_20_percent(self):
        cost, _ = calculate_delivery_cost(5.1, 100, "обычный")
        # ожидаем 700 * 1.2 = 840
        self.assertEqual(cost, 840)

    def test_boundary_weight_exactly_5_should_get_surcharge(self):
        """🐛 БАГ: weight=5.0 должен давать надбавку 1.2, но не даёт"""
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        # ожидаем 700 * 1.2 = 840, но получим 700
        self.assertEqual(cost, 840)

    def test_heavy_weight_surcharge_50_percent(self):
        cost, _ = calculate_delivery_cost(25, 100, "обычный")
        # ожидаем 700 * 1.5 = 1050
        self.assertEqual(cost, 1050)

    def test_fragile_package_adds_300(self):
        cost, _ = calculate_delivery_cost(3, 100, "хрупкий")
        # 700 + 300 = 1000
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000(self):
        cost, _ = calculate_delivery_cost(3, 100, "опасный")
        # 700 + 1000 = 1700
        self.assertEqual(cost, 1700)

    def test_express_should_be_more_expensive(self):
        """🐛 БАГ: экспресс умножается на 0.5 — становится ДЕШЕВЛЕ"""
        normal_cost, _ = calculate_delivery_cost(3, 100, "обычный")
        express_cost, _ = calculate_delivery_cost(3, 100, "обычный", is_express=True)
        # ожидаем, что экспресс дороже обычной доставки
        self.assertGreater(express_cost, normal_cost)


class TestDeliveryDate(unittest.TestCase):
    """Тесты расчёта даты доставки"""

    def test_short_distance_takes_one_day(self):
        _, date = calculate_delivery_cost(3, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_500_takes_one_day(self):
        _, date = calculate_delivery_cost(3, 500, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_1000_takes_two_days(self):
        _, date = calculate_delivery_cost(3, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_express_delivery_is_faster(self):
        _, normal_date = calculate_delivery_cost(3, 2000, "обычный")
        _, express_date = calculate_delivery_cost(3, 2000, "обычный", is_express=True)
        # экспресс должен быть раньше
        self.assertLess(express_date, normal_date)

    def test_express_minimum_one_day(self):
        """🐛 БАГ: для distance=500 экспресс даёт 0 дней (1//2=0)"""
        _, date = calculate_delivery_cost(3, 500, "обычный", is_express=True)
        # ожидаем минимум 1 день → 2026-09-04, а не 2026-09-03
        self.assertEqual(date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()