from unittest import TestCase, mock

from src.model import MyUserModel, LocalDataBaseModel, User

class MyUserModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_model = MyUserModel(db_model=LocalDataBaseModel())

    @mock.patch('src.model.LocalDataBaseModel.get_user', return_value={
        "user_name": "Guile",
        "user_email": "guile@gmail.com",
        "user_language": "French",
        "user_photo": "photo.com/guile"
    })
    def test_get_user(self, db_get_user):
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