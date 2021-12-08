from unittest import TestCase, mock

from src.controller import MyUserController
from src.model import UserModel

class MyUserControllerTestCase (TestCase):

    @classmethod
    def SetUpClass(cls):
        self.user_controller = MyUserController(user_model=UserModel())

    @mock.patch("MyUserContoller.user_model.get_user_id", return_value=10)
    def test_login(self):
        self.assertEqual(
            self.user_controller.res_login(user_email="test@google.com", password="pass1234"),
            0
        )