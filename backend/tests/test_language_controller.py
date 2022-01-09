from unittest import TestCase, mock

from src.controller import LanguageController, MyLanguageController
from src.model import WordInfo
from src.model.exceptions import LanguageNotSupportedError, UserIdError, WordDoesNotExistError, TranslationNotFound, TranslationApiConnectionError, NlpCalculationError

"""
Lacking implementation:
- type checking of the inputs
- differenciating between server error and db error (in all tests and controllers)
"""


class MyLanguageControllerTestCase(TestCase):

    def setUp(self):
        patcher_words_model = mock.patch('src.model.DummyWordsModel')
        patcher_translation_model = mock.patch('src.model.TranslationModel')
        patcher_nlp_model = mock.patch('src.model.DummyNlpModel')

        self.mock_words_model = patcher_words_model.start()
        self.mock_translation_model = patcher_translation_model.start()
        self.mock_nlp_model = patcher_nlp_model.start()

        def cleanup():
            patcher_words_model.stop()
            patcher_translation_model.stop()
            patcher_nlp_model.stop()
        self.addCleanup(cleanup)

        self.language_controller: LanguageController = MyLanguageController(
            words_model=self.mock_words_model,
            translation_model=self.mock_translation_model, 
            nlp_model=self.mock_nlp_model,
            supported_languages=[
                {
                    "name": "English",
                    "flag": "🇬🇧",
                    "code": "en"
                }
            ],
            conversion_function=lambda x: 10
        )

        self.mock_words_model.get_word_and_language.return_value = WordInfo("Cat", "English")
        self.mock_nlp_model.calculate_similarity.return_value = 0.5
        self.mock_translation_model.translate.return_value = "House"

    def test_add_words(self):
        self.mock_words_model.add_words.return_value = None
        self.assertEqual(
            self.language_controller.res_add_words.callable(
                self.language_controller,
                1,
                ["House", "Pig", "Pencil"]
            ),
            {
                "code": 1,
                "message": "Words added successfully."
            }
        )

    def test_add_words_user_not_found(self):
        self.mock_words_model.add_words.side_effect = UserIdError("ops...")
        self.assertEqual(
            self.language_controller.res_add_words.callable(
                self.language_controller,
                10,
                ["House", "Pig", "Pencil"]
            ),
            {
                "code": -5,
                "message": "The desired user was not found in the database."
            }

        )
    
    def test_add_words_server_error(self):
        self.mock_words_model.add_words.side_effect = Exception("ops...")
        self.assertEqual(
            self.language_controller.res_add_words.callable(
                self.language_controller,
                1,
                ["House", "Plant"]
            ),
            {
                "code": -12,
                "message": "An error occured in the database."
            }
        )

    def test_get_words_from_user(self):
        self.mock_words_model.get_words_from_user.return_value = ["House", "Plant", "Pig"]
        self.assertEqual(
            self.language_controller.res_get_words_from_user.callable(
                self.language_controller,
                1
            ),
            {
                "code": 1,
                "message": "Words fetched successfully.",
                "words": ["House", "Plant", "Pig"]
            }
        )

    def test_get_words_from_user_id_error(self):
        self.mock_words_model.get_words_from_user.side_effect = UserIdError("ops...")
        self.assertEqual(
            self.language_controller.res_get_words_from_user.callable(
                self.language_controller,
                1
            ),
            {
                "code": -5,
                "message": "The desired user was not found in the database."
            }
        )
    
    def test_get_words_from_user_server_error(self):
        self.mock_words_model.get_words_from_user.side_effect = Exception("ops...")
        self.assertEqual(
            self.language_controller.res_get_words_from_user.callable(
                self.language_controller,
                1
            ),
            {
                "code": -12,
                "message": "An error occured in the database."
            }
        )
    
    def test_res_calculate_score(self):
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": 1,
                "message": "Score calculated successfully.",
                "score": 0.5
            }
        )

    def test_res_calculate_score_word_dont_exist(self):
        self.mock_words_model.get_word_and_language.side_effect = WordDoesNotExistError("ops...")
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": -8,
                "message": "No word with the given ID could be found in the database."
            }
        )

    def test_res_calculate_score_user_dont_exist(self):
        self.mock_words_model.get_word_and_language.side_effect = UserIdError("ops...")
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": -1,
                "message": "The related user could not be found in the database."
            }
        )
    
    def test_res_calculate_score_translation_not_found(self):
        self.mock_translation_model.translate.side_effect = TranslationNotFound("ops...")
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": -9,
                "message": "The given word could not be translated."
            }
        )
    
    def test_res_calculate_score_translator_connection_error(self):
        self.mock_translation_model.translate.side_effect = TranslationApiConnectionError("ops...")
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": -10,
                "message": "Connection with the translator could not be made."
            }
        )
    
    def test_res_calculate_score_nlp_calculation_error(self):
        self.mock_nlp_model.calculate_similarity.side_effect = NlpCalculationError("ops...")
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": -11,
                "message": "The NLP model could not calculate your request."
            }
        )

    def test_res_calculate_score_server_error(self):
        self.mock_words_model.get_word_and_language.side_effect = Exception("ops...")
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": -12,
                "message": "An error occured in the database."
            }
        )

    def test_res_calculate_score_language_not_supported(self):
        self.mock_translation_model.translate.side_effect = LanguageNotSupportedError("ops...")
        self.assertEqual(
            self.language_controller.res_calculate_score.callable(
                self.language_controller,
                1,
                "Casa"
            ),
            {
                "code": -14,
                "message": "The desired language is not supported."
            }
        )
        