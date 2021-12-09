from unittest import TestCase

from src.model import LocalDataBaseModel, PostgresqlDataBaseModel
from src.model.exceptions import UserIdError, PropertyNotValidError, UserNotFoundError, ValueTypeNotValidError, UserAlreadyExistsError

from src.model.db_model import parse_postgresql_url


class PostgresqlDataBaseModelTestCase(TestCase):

    def test_url_parsing(self):
        result = parse_postgresql_url(
            "postgres://username:password@asd-10-10-100-100-100.computer-1.amazonaws.com:5000/databasename"
        )
        self.assertEqual(
            result,
            {
                "user": "username",
                "password": "password",
                "host": "asd-10-10-100-100-100.computer-1.amazonaws.com",
                "port": 5000,
                "database": "databasename"
            }    
        )


class LocalDbModelTestCase(TestCase):

    def setUp(self):
        self.database = LocalDataBaseModel()

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

    def test_add_user_already_exists(self):
        self.assertRaises(
            UserAlreadyExistsError,
            self.database.add_user,
            user_name="Guile",
            user_email="test@gmail.com",
            user_password="senha1234",
            user_language="Portuguese"
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
        user_id = self.database.find_user(properties={
            "user_name": "test"
        })
        self.assertEqual(user_id, 0)
        user_id = self.database.find_user(properties={
            "user_email": "test@gmail.com",
            "user_password": "pass1234"
        })

    def test_find_user_property_not_valid(self):
        self.assertRaises(
            PropertyNotValidError,
            self.database.find_user,
            properties={
                "user_surname": "asdf"
            }
        )

    def test_find_user_value_type_not_valid(self):
        self.assertRaises(
            ValueTypeNotValidError,
            self.database.find_user,
            properties={
                "user_name": 12
            }
        )
    
    def test_find_user_no_matches(self):
        self.assertRaises(
            UserNotFoundError,
            self.database.find_user,
            properties={
                "user_email": "email_not_existant@gmail.com"
            }
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