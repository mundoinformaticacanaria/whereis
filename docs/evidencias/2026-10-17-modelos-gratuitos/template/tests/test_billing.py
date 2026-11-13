import unittest
from src.billing import discounted_cents

class BillingTests(unittest.TestCase):
    def test_zero_discount(self):
        self.assertEqual(discounted_cents(100, 0), 100)
