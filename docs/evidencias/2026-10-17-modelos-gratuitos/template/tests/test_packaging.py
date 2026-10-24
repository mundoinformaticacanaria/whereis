import unittest
from src.packaging import package_label

class PackagingTests(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(package_label("BOX"), "BOX")
