from unittest import TestCase, mock

from src.model import GoogleTranslationModel, LingueeTranslationModel
from src.model.translation_model.deep_translator.exceptions import LanguageNotSupportedException
from src.model.exceptions import LanguageNotSupportedError

class GoogleTranslationModelTestCase(TestCase):

    def setUp(self) -> None:
        patcher = mock.patch("src.model.translation_model.googletrans.Translator")
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

    
class LingueeTranslationModelTestCase(TestCase):

    def setUp(self) -> None:
        linguee_patcher = mock.patch("src.model.translation_model.deep_translator.LingueeTrasnslator")
        google_patcher = mock.patch("src.model.translation_model.googletrans.Translator")
        self.mock_linguee = linguee_patcher.start()
        self.mock_google = google_patcher.start()
        self.addCleanup(linguee_patcher.stop)
        self.addCleanup(google_patcher.stop)

        self.detector = self.mock_google.return_value.detect
        self.translator = self.mock_linguee.return_value.translate

        self.linguee_translation_model= LingueeTranslationModel()
    
    def test_translate_language_not_supported(self):
        self.detector.return_value = "aa"
        self.translator.side_effect = LanguageNotSupportedException
        self.assertRaises(
            LanguageNotSupportedError,
            self.linguee_translation_model.translate,
            to_language="en",
            word="Casa"
        )

        