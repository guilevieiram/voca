from unittest import TestCase, mock

from src.model import SpacyNlpModel, NltkNlpModel
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
    
class NltkNlpModelTestcase(TestCase):

    def setUp(self) -> None:
       patcher = mock.patch("src.model.nlp_model.nltk") 
       self.mock_nltk = patcher.start()
       self.addCleanup(patcher.stop)

       self.similarity = self.mock_nltk.corpus.wordnet.synsets.return_value[0].wup_similarity
       self.mock_nltk.download.return_value = None

       self.nlp_model = NltkNlpModel(
           supported_languages=["en"]
       )
    
    def test_translate(self):
        self.similarity.return_value = 0.8
        self.assertEqual(
            self.nlp_model.calculate_similarity(
                "rat",
                ["cat", "kitty"],
                language="en"
            ),
            0.8
        )
        self.assertEqual(
            self.nlp_model.calculate_similarity(
                ["rat", "mouse"],
                ["cat", "kitty"],
                language="en"
            ),
            0.8
        )
        self.assertEqual(
            self.nlp_model.calculate_similarity(
                ["rat", "mouse"],
                "cat",
                language="en"
            ),
            0.8
        )
        self.assertEqual(
            self.nlp_model.calculate_similarity(
                "rat",
                "cat",
                language="en"
            ),
            0.8
        )

    def test_language_not_supported(self):
        self.assertRaises(
            LanguageNotSupportedError,
            self.nlp_model.calculate_similarity,
            first="rat",
            second=["cat", "kitty"],
            language="fr"
        )
    