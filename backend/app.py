# To deploy on heroku, run from the root app directory the command
# git subtree push --prefix backend heroku main
from typing import List, Dict

from config import Configurations

from src.controller import MainController, FlaskController, TerminalController
from src.controller import UserController, MyUserController, DummyUserController
from src.controller import LanguageController, MyLanguageController, DummyLanguageController
from src.model import UserModel, MyUserModel
from src.model import DataBaseModel, LocalDataBaseModel, PostgresqlDataBaseModel
from src.model import WordsModel, MyWordsModel
from src.model import TranslationModel, DummyTranslationModel, GoogleTranslationModel
from src.model import NlpModel, DummyNlpModel, SpacyNlpModel
from src.model import ConversionFunction, FloorConversion

database_model: DataBaseModel = PostgresqlDataBaseModel()

user_model: UserModel = MyUserModel
nlp_model: NlpModel = DummyNlpModel
translation_model: TranslationModel = DummyTranslationModel
words_model: WordsModel = MyWordsModel
user_controller: UserController = MyUserController
language_controller: LanguageController = MyLanguageController
main_controller: MainController = FlaskController

supported_languages: List[Dict[str, str]] = Configurations.supported_languages
supported_languages_codes: List[str] = Configurations.supported_languages_codes
conversion: ConversionFunction = FloorConversion

endpoint = main_controller(
    user_controller=user_controller(
        user_model=user_model(
            database_model=database_model,
            supported_languages_codes=supported_languages_codes
        )
    ),
    language_controller=language_controller(
        words_model=words_model(
            database_model=database_model
        ),
        translation_model=translation_model(),
        nlp_model=nlp_model(supported_languages=supported_languages_codes),
        supported_languages=supported_languages,
        conversion_function=conversion.calculate
    )
)
app = endpoint.app

if __name__ == "__main__":
    endpoint.run(debug=Configurations.debug)
