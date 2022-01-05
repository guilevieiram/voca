from unittest import TestCase, mock

from src.model import GoogleTranslationModel
from src.model.exceptions import LanguageNotSupportedError

class GoogleTranslationModelTestCase(TestCase):

    def setUp(self) -> None:
        patcher = mock.patch("src.model.translation_model.Translator")
        self.mock_translator = patcher.start()
        self.addCleanup(patcher.stop)
        self.google_translation_model = GoogleTranslationModel()

    def test_translate_language_not_supported(self):
        self.mock_translator.return_value.translate.side_effect = ValueError("ops...")
        self.assertRaises(
            LanguageNotSupportedError,
            self.google_translation_model.translate,
            to_language="aa",
            word="House"
        )

        