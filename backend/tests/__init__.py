"""
This is the testing module for the application.
For every component tested, please add the imports here so we can have a controlled approach
in all the tests.
"""

from .test_db_model import LocalDbModelTestCase
from .test_db_model import PostgresqlDataBaseModelTestCase
from .test_user_model import MyUserModelTestCase
from .test_user_model import HashUserModelTestCase
from .test_translation_model import GoogleTranslationModelTestCase
from .test_translation_model import LingueeTranslationModelTestCase
from .test_nlp_model import SpacyNlpModelTestCase
from .test_nlp_model import NltkNlpModelTestcase

from .test_functions import FloorConversionTestCase

from .test_user_controller import MyUserControllerTestCase
from .test_language_controller import MyLanguageControllerTestCase
