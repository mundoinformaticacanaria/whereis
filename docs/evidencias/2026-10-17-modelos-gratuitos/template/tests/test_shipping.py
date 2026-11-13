import unittest
from src.shipping import shipping_cents

class ShippingTests(unittest.TestCase):
    def test_small_order(self):
        self.assertEqual(shipping_cents(900), 500)
