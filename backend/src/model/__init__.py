"""
This is the models module of your application. Here you should develop the different models your controller might need.
After constructing them in a separate file, import them here, both the abstract form and the implementations.
"""

from .user_model import User, UserModel, MyUserModel, HashedUserModel
from .database_model import DataBaseModel, LocalDataBaseModel, PostgresqlDataBaseModel
from .nlp_model import NlpModel, DummyNlpModel, SpacyNlpModel, NltkNlpModel
from .translation_model import TranslationModel, DummyTranslationModel, GoogleTranslationModel, LingueeTranslationModel

from .words_model import WordsModel, DummyWordsModel, MyWordsModel, WordInfo

from .functions import ConversionFunction, FloorConversion
