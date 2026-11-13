import unittest
from src.allocations import split_cents

class AllocationTests(unittest.TestCase):
    def test_even(self):
        self.assertEqual(split_cents(6, 3), [2, 2, 2])
