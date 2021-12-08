from unittest import TestCase, mock

from src.controller import MyUserController
from src.model import UserModel, User
from src.model.exceptions import WrongPasswordError, UserAlreadyExistsError, UserIdError, PropertyNotValidError, ValueTypeNotValidError

class MyUserControllerTestCase (TestCase):

    def setUp(self):
        patcher = mock.patch('src.model.MyUserModel')
        self.mock_user_model = patcher.start()
        self.addCleanup(patcher.stop)
        self.user_controller = MyUserController(self.mock_user_model)

    def test_login(self):
        self.mock_user_model.get_user_id.return_value = 0
        self.assertEqual(
            self.user_controller.res_login.callable(
                self=self.user_controller,
                user_email="gui@google.com",
                password="1234"
            ),
            {
                "code": 1,
                "message": "Login successful.",
                "id": 0
            }
        )

    def test_login_wrong_password(self):
        self.mock_user_model.get_user_id.side_effect = WrongPasswordError("Wrong password!!")
        self.assertEqual(
            self.user_controller.res_login.callable(
                self=self.user_controller,
                user_email="gui@google.com",
                password="1234"
            ),
            {
                "code": -2,
                "message": "Wrong password."
            }
        )

    def test_login_databse_error(self):
        self.mock_user_model.get_user_id.side_effect = Exception("Something happened!")
        self.assertEqual(
            self.user_controller.res_login.callable(
                self=self.user_controller,
                user_email="gui@google.com",
                password="1234"
            ),
            {
                "code": -3,
                "message": "A problem occured with the database."
            }
        )
    
    def test_sign_up(self):
        self.mock_user_model.add_user.return_value = None
        self.assertEqual(
            self.user_controller.res_sign_up.callable(
                self=self.user_controller,
                user_name="Gui",
                user_email="gui@gmail.com",
                user_password="asdf",
                user_language="Chinese"
            ),
            {
                "code": 1,
                "message": "User added with no problem."
            }
        )   
        self.assertEqual(
            self.user_controller.res_sign_up.callable(
                self=self.user_controller,
                user_name="Gui",
                user_email="gui@gmail.com",
                user_password="asdf",
                user_language="Chinese",
                user_photo="google.com"
            ),
            {
                "code": 1,
                "message": "User added with no problem."
            }
        )
    
    def test_sign_up_user_already_exists(self):
        self.mock_user_model.add_user.side_effect = UserAlreadyExistsError("oops...")
        self.assertEqual(
            self.user_controller.res_sign_up.callable(
                self=self.user_controller,
                user_name="Gui",
                user_email="gui@gmail.com",
                user_password="asdf",
                user_language="Chinese",
            ),
            {
                "code": -6,
                "message": "This user email is already in use."
            }
        )
    
    def test_sign_up_db_error(self):
        self.mock_user_model.add_user.side_effect = Exception("oops...")
        self.assertEqual(
            self.user_controller.res_sign_up.callable(
                self=self.user_controller,
                user_name="Gui",
                user_email="gui@gmail.com",
                user_password="asdf",
                user_language="Chinese",
            ),
            {
                "code": -3,
                "message": "A problem occured in the database."
            }
        )
        
    def test_delete_user(self):
        self.mock_user_model.delete_user.return_value = None
        self.assertEqual(
            self.user_controller.res_delete_user.callable(
                self=self.user_controller,
                user_id=10
            ),
            {
                "code": 1,
                "message": "User deleted."
            }
        )
    
    def test_delete_user_not_exists(self):
        self.mock_user_model.delete_user.side_effect = UserIdError
        self.assertEqual(
            self.user_controller.res_delete_user.callable(
                self=self.user_controller,
                user_id=10
            ),
            {
                "code": -5,
                "message": "Given user id is not valid."
            }
        )

    def test_delete_user_db_error(self):
        self.mock_user_model.delete_user.side_effect = Exception("oops...")
        self.assertEqual(
            self.user_controller.res_delete_user.callable(
                self=self.user_controller,
                user_id=10
            ),
            {
                "code": -3,
                "message": "A problem occured in the database."
            }
        )

    def test_get_user(self):
        self.mock_user_model.get_user.return_value = User(
            id=10,
            name="Guile",
            email="guile@gmail.com",
            language="Chinese",
            photo_url="google.com/pic"
        )
        self.assertEqual(
            self.user_controller.res_get_user.callable(
                self=self.user_controller,
                user_id=10
            ),
            {
                "code": 1,
                "message": "User data fetched with success.",
                "user": {
                    "name": "Guile",
                    "email": "guile@gmail.com",
                    "language": "Chinese",
                    "photo_url": "google.com/pic"   
                }
            }
        )
    
    def test_get_user_user_id_error(self):
        self.mock_user_model.get_user.side_effect = UserIdError("oops...")
        self.assertEqual(
            self.user_controller.res_get_user.callable(
                self=self.user_controller,
                user_id=10
            ),
            {
                "code": -5,
                "message": "Given user id is not valid."
            }
        )
    
    def test_get_user_db_error(self):
        self.mock_user_model.get_user.side_effect = Exception("oops...")
        self.assertEqual(
            self.user_controller.res_get_user.callable(
                self=self.user_controller,
                user_id=10
            ),
            {
                "code": -3,
                "message": "A problem occured in the database."
            }
        )

    def test_update_user(self):
        self.mock_user_model.update_user.return_value = None
        self.assertEqual(
            self.user_controller.res_update_user.callable(
                self=self.user_controller,
                user_id=10,
                property="user_name",
                value="Pierre"
            ),
            {
                "code": 1,
                "message": "User successfully updated."
            }
        )

    def test_update_user_id_error(self):
        self.mock_user_model.update_user.side_effect = UserIdError("ops...")
        self.assertEqual(
            self.user_controller.res_update_user.callable(
                self=self.user_controller,
                user_id=10,
                property="user_name",
                value="Pierre"
            ),
            {
                "code": -5,
                "message": "Given user id is not valid."
            }
        )

    def test_update_user_property_error(self):
        self.mock_user_model.update_user.side_effect = PropertyNotValidError("ops...")
        self.assertEqual(
            self.user_controller.res_update_user.callable(
                self=self.user_controller,
                user_id=10,
                property="user_name",
                value="Pierre"
            ),
            {
                "code": -4,
                "message": "The given property is not valid."
            }
        )

    def test_update_user_value_error(self):
        self.mock_user_model.update_user.side_effect = PropertyNotValidError("ops...")
        self.assertEqual(
            self.user_controller.res_update_user.callable(
                self=self.user_controller,
                user_id=10,
                property="user_name",
                value="Pierre"
            ),
            {
                "code": -7,
                "message": "The wanted value is not from the right type."
            }
        )

    def test_update_user_db_error(self):
        self.mock_user_model.update_user.side_effect = Exception("ops...")
        self.assertEqual(
            self.user_controller.res_update_user.callable(
                self=self.user_controller,
                user_id=10,
                property="user_name",
                value="Pierre"
            ),
            {
                "code": -3,
                "message": "A problem occured in the database."
            }
        )