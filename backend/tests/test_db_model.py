import unittest
from unittest.mock import patch

from src.model import LocalDataBase


class LocalDbModelTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.database = LocalDataBase()

    def test_add_user(self):
        self.database.add_user(
            user_name = "guilherme",
            user_email= "guilhermevmanhaes@gmail.com",
            user_password="shittypass",
            user_photo="https://photo.com"
        )
        self.assertEqual(
            self.database.users[1], 
            {
                "user_name": "guilherme",
                "user_email": "guilhermevmanhaes@gmail.com",
                "user_password": "shittypass",
                "user_photo":"https://photo.com"
            }
        )

