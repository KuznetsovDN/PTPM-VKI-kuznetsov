import unittest
import sys
import os



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Delivery import calculate_delivery_cost

class TestDeliveryMethods (unittest.TestCase):

    def test_1(self):
        cost, _ = calculate_delivery_cost(0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_2(self):
        cost, _ = calculate_delivery_cost(25, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_3(self):
        cost, _ = calculate_delivery_cost(5, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_4(self):
        cost, _ = calculate_delivery_cost(25, 100, "обычный")
        self.assertEqual(cost, 1050)
if __name__ == "__main__":
    unittest.main()