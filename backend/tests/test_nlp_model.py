from unittest import TestCase, mock

from src.model import SpacyNlpModel
from src.model.exceptions import LanguageNotSupportedError

class SpacyNlpModelTestCase(TestCase):

    def setUp(self) -> None:
        patcher = mock.patch("src.model.nlp_model.spacy")
        self.mock_spacy = patcher.start()
        self.addCleanup(patcher.stop)

        supported_languages = ["en", "pt", "fr", "ru", "zh-CN"]
        self.nlp_model = SpacyNlpModel(supported_languages=supported_languages)

    def test_calculate_similarity(self):
        self.mock_spacy.load.return_value.return_value.similarity.return_value = 0.123
        self.assertEqual(
            self.nlp_model.calculate_similarity("word", "word", "en"),
            0.123
        )
        
    def test_calculate_similarity_wrong_parameters(self):
        self.assertRaises(
            TypeError,
            self.nlp_model.calculate_similarity,
            "word", 
            5, 
            "en"
        )
    
    def test_calculate_similarity_language_not_supported(self):
        self.assertRaises(
            LanguageNotSupportedError,
            self.nlp_model.calculate_similarity,
            "word",
            "word",
            "aa"
        )
    
    
