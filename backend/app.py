# To deploy on heroku, run from the root app directory the command
# git subtree push --prefix backend heroku main

from config import Configurations

from src.controller import MainController, FlaskController, TerminalController
from src.controller import UserController, MyUserController, DummyUserController
from src.controller import LanguageController, MyLanguageController
from src.model import UserModel, MyUserModel
from src.model import DataBaseModel, LocalDataBaseModel, PostgresqlDataBaseModel
from src.model import WordsModel, MyWordsModel
from src.model import TranslationModel, DummyTranslationModel
from src.model import NlpModel, DummyNlpModel

database_model: DataBaseModel = PostgresqlDataBaseModel()
user_model: UserModel = MyUserModel
nlp_model: NlpModel = DummyNlpModel
translation_model: TranslationModel = DummyTranslationModel
words_model: WordsModel = MyWordsModel
user_controller: UserController = MyUserController
language_controller: LanguageController = MyLanguageController
main_controller: MainController = FlaskController

endpoint = main_controller(
    user_controller=user_controller(
        user_model=user_model(
            database_model=database_model,
            supported_languages=Configurations.supported_languages_codes
        )
    ),
    language_controller=language_controller(
        words_model=words_model(
            database_model=database_model
        ),
        translation_model=translation_model(),
        nlp_model=nlp_model()
    )
)
app = endpoint.app

if __name__ == "__main__":
    endpoint.run()