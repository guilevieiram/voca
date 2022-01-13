# To deploy on heroku, run from the root app directory the command
# git subtree push --prefix backend heroku main

from typing import List, Dict
import logging

from config import Configurations

from src.controller import MainController, FlaskController, TerminalController
from src.controller import UserController, MyUserController, DummyUserController
from src.controller import LanguageController, MyLanguageController, DummyLanguageController, SimpleLanguageController

from src.model import UserModel, MyUserModel
from src.model import DataBaseModel, LocalDataBaseModel, PostgresqlDataBaseModel
from src.model import WordsModel, MyWordsModel
from src.model import TranslationModel, DummyTranslationModel, GoogleTranslationModel, LingueeTranslationModel
from src.model import NlpModel, DummyNlpModel, SpacyNlpModel, NltkNlpModel
from src.model import ConversionFunction, FloorConversion


# -----------------------------------------------------------
# Getting configurations 
# -----------------------------------------------------------
database_url: str = Configurations.database_url
debug: bool = Configurations.debug
supported_languages: List[Dict[str, str]] = Configurations.supported_languages
supported_languages_codes: List[str] = Configurations.supported_languages_codes
user_logger: logging.Logger = Configurations.logger(name="user")
language_logger: logging.Logger = Configurations.logger(name="language")

conversion: ConversionFunction = FloorConversion

# -----------------------------------------------------------
# Defining the controllers and models to be used
# -----------------------------------------------------------

database_model: DataBaseModel = PostgresqlDataBaseModel(database_url=database_url)

user_model:             UserModel =             MyUserModel
nlp_model:              NlpModel =              NltkNlpModel
translation_model:      TranslationModel =      LingueeTranslationModel
words_model:            WordsModel =            MyWordsModel
user_controller:        UserController =        MyUserController
language_controller:    LanguageController =    SimpleLanguageController
main_controller:        MainController =        FlaskController


# -----------------------------------------------------------
# Initializing application
# -----------------------------------------------------------

endpoint = main_controller(
    user_controller=user_controller(
        user_model=user_model(
            database_model=database_model,
            supported_languages_codes=supported_languages_codes
        ),
        logger=user_logger
    ),
    language_controller=language_controller(
        words_model=words_model(
            database_model=database_model
        ),
        translation_model=translation_model(),
        nlp_model=nlp_model(supported_languages=supported_languages_codes),
        supported_languages=supported_languages,
        conversion_function=conversion.calculate,
        logger=language_logger
    )
)


# Defining the app object to be read by Heroku
app = endpoint.app

# Running the app in the local machine
if __name__ == "__main__":
    endpoint.run(debug=debug)
