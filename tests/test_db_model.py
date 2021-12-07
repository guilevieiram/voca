import unittest
from unittest.mock import patch

from src.model import LocalDataBase
from src.model.exceptions import UserIdError, PropertyNotValidError, UserNotFoundError, ValueTypeNotValidError


class LocalDbModelTestCase(unittest.TestCase):

    def setUp(self):
        self.database = LocalDataBase()

    def test_add_user(self):
        self.database.add_user(
            user_name ="guilherme",
            user_email="guilhermevmanhaes@gmail.com",
            user_language="French",
            user_password="shittypass",
            user_photo="https://photo.com"
        )
        self.assertEqual(
            self.database.users[1], 
            {
                "user_name": "guilherme",
                "user_email": "guilhermevmanhaes@gmail.com",
                "user_language": "French",
                "user_password": "shittypass",
                "user_photo":"https://photo.com"
            }
        )
    
    def test_delete_user(self):
        self.database.delete_user(user_id = 0)
        self.assertIsNone(self.database.users[0])

    def test_delete_user_not_fount(self):
        self.assertRaises(
            UserIdError,
            self.database.delete_user,
            user_id=10
        )
    
    def test_find_user(self):
        user_id = self.database.find_user(
            property="user_name",
            value="test"
        )
        self.assertEqual(user_id, 0)

    def test_find_user_property_not_valid(self):
        self.assertRaises(
            PropertyNotValidError,
            self.database.find_user,
            property="user_surname", 
            value="asdf"
        )

    def test_find_user_value_type_not_valid(self):
        self.assertRaises(
            ValueTypeNotValidError,
            self.database.find_user,
            property="user_name",
            value=12
        )
    
    def test_find_user_no_matches(self):
        self.assertRaises(
            UserNotFoundError,
            self.database.find_user,
            property="user_email",
            value="email_not_existant@gmail.com"
        )

    def  test_update_user(self):
        self.database.update_user(
            user_id=0,
            property="user_email",
            value="google.gmail.com"
        )
        self.assertEqual(self.database.users[0]["user_email"], "google.gmail.com")

    def test_update_user_no_matches(self):
        self.assertRaises(
            UserIdError,
            self.database.update_user,
            user_id=10,
            property="user_name",
            value="carlos"
        )
        self.database.users[0] = None
        self.assertRaises(
            UserIdError,
            self.database.update_user,
            user_id=0,
            property="user_name",
            value="Carlos"
        )

    def test_update_user_property_not_valid(self):
        self.assertRaises(
            PropertyNotValidError,
            self.database.update_user,
            user_id=0,
            property="user_surname",
            value="Martins"
        )

    def test_update_user_value_type_not_valid(self):
        self.assertRaises(
            ValueTypeNotValidError,
            self.database.update_user,
            user_id=0,
            property="user_name",
            value=12
        )

    def test_get_user(self):
        user = self.database.get_user(user_id=0)
        self.assertEqual(
            user, 
            {
                "user_name": "test",
                "user_email": "test@gmail.com",
                "user_photo": "ph.com",
                "user_language": "Testuguese"
            }
        )

    def test_get_user_no_matches(self):
        self.assertRaises(
            UserIdError,
            self.database.get_user,
            user_id=10
        )
        self.database.users[0] = None
        self.assertRaises(
            UserIdError,
            self.database.get_user,
            user_id=0
        )