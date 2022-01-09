from unittest import TestCase

from src.model import FloorConversion

class FloorConversionTestCase(TestCase):

    def test_calculate(self):
        self.assertEqual(
            FloorConversion.calculate(0.356),
            35
        )
        self.assertEqual(
            FloorConversion.calculate(0),
            0 
        )
        self.assertEqual(
            FloorConversion.calculate(1),
            100 
        )
        self.assertEqual(
            FloorConversion.calculate(0.5),
            50 
        )