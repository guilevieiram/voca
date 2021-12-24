from unittest import TestCase, mock

from src.model import MyUserModel, LocalDataBaseModel, User
from src.model.exceptions import UserNotFoundError, WrongPasswordError

class MyUserModelTestCase(TestCase):

    def setUp(self):
        patcher = mock.patch('src.model.LocalDataBaseModel')
        self.mock_db_model = patcher.start()
        self.addCleanup(patcher.stop)
        self.user_model = MyUserModel(db_model=self.mock_db_model)

    def test_get_user(self):
        self.mock_db_model.get_user.return_value = {
            "user_name": "Guile",
            "user_email": "guile@gmail.com",
            "user_language": "French",
            "user_photo": "photo.com/guile"
        }
        self.assertEqual(
            self.user_model.get_user(user_id=10),
            User(
                id=10,
                name="Guile",
                email="guile@gmail.com",
                language="French",
                photo_url="photo.com/guile"
            )
        )
    
    def test_login_user(self):
        self.mock_db_model.find_user.return_value = 10
        self.assertEqual(
            self.user_model.login_user(
                user_email="test@gmail.com",
                user_password="pass1234"
            ),
            10
        )
    
    def test_login_user_not_valid(self):
        self.mock_db_model.find_user.side_effect = UserNotFoundError("ops ... ")
        self.assertRaises(
            UserNotFoundError,
            self.user_model.login_user,
            user_email="test@gmail.com",
            user_password="pass1234"
        )

    def test_login_user_not_valid(self):
        self.mock_db_model.find_user.side_effect = WrongPasswordError("ops ... ")
        self.assertRaises(
            WrongPasswordError,
            self.user_model.login_user,
            user_email="test@gmail.com",
            user_password="pass1234"
        )