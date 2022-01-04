"""
This is the testing module for the application.
For every component tested, please add the imports here so we can have a controlled approach
in all the tests.
"""
from .test_db_model import LocalDbModelTestCase
from .test_user_model import MyUserModelTestCase
from .test_user_controller import MyUserControllerTestCase
from .test_db_model import PostgresqlDataBaseModelTestCase
from .test_language_controller import MyLanguageControllerTestCase