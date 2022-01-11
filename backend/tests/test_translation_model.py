from unittest import TestCase, mock

import deep_translator

from src.model import GoogleTranslationModel, LingueeTranslationModel
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

    def test_translate_all_translations(self):
        self.mock_translator.return_value.translate.return_value = "word"
        self.assertIsInstance(
            self.google_translation_model.translate(
                to_language="en",
                word="Casa",
                all_translations=True
            ),
            list
        )

    
class LingueeTranslationModelTestCase(TestCase):

    def setUp(self) -> None:
        deep_translator_patcher = mock.patch("src.model.translation_model.deep_translator")
        googletrans_patcher = mock.patch("src.model.translation_model.googletrans")
        self.mock_deep_translator = deep_translator_patcher.start()
        self.mock_googletrans = googletrans_patcher.start()
        self.addCleanup(deep_translator_patcher.stop)
        self.addCleanup(googletrans_patcher.stop)

        self.mock_detector = self.mock_googletrans.Translator.return_value.detect
        self.mock_translator = self.mock_deep_translator.LingueeTranslator
        self.mock_detector.return_value = "aa"

        self.linguee_translation_model= LingueeTranslationModel()
    
    def test_translate_language_not_supported(self):
        self.mock_translator.side_effect = Exception("ops..")
        self.assertRaises(
            LanguageNotSupportedError,
            self.linguee_translation_model.translate,
            to_language="en",
            word="Casa"
        )

        