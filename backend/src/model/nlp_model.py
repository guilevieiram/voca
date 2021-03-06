from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union

import spacy
import nltk

from src.model.exceptions import LanguageNotSupportedError

class NlpModel(ABC):
    """Abstract model class to handle Natural Language Processing related tasks."""

    @abstractmethod
    def calculate_similarity(self, first: Union[str, List[str]], second: Union[str, List[str]], language: str) -> float:
        """Calculates the similarity between two words, or two list of words, returning the best result."""


class DummyNlpModel(NlpModel):
    """Dummy model class to handle Natural Language Processing related tasks."""

    def __init__(self, *args, **kwargs) -> None:
        """Dummy init method to get whatever parameters"""

    def calculate_similarity(self, first: Union[str, List[str]], second: Union[str, List[str]], language: str) -> float:
        """Calculates the similarity between two words, or two list of words, returning the best result."""
        return 0.98


class SpacyNlpModel(NlpModel):
    """Concrete model class to handle Natural Language Processing related tasks implemented using Spacy."""

    def __init__(self, supported_languages: List[str]) -> None:
        """Initializer to import the necessary spacy models."""

        languages_models_mapping: dict[str, str] = {
            "en": "en_core_web_md",
            "fr": "fr_core_news_md",
            "ru": "ru_core_news_md",
            "pt": "pt_core_news_md",
            "zh-CN": "zh_core_web_md"
        }
        self.nlp: Dict[str, Any] = {} # dictionary to encapsulate all the loaded modules
        for language in supported_languages:
            self.nlp[language] = spacy.load(
                languages_models_mapping[language],
                disable=["tagger", "parser", "attribute_ruler", "lemmatizer", "ner"]
            )

    def calculate_similarity(self, first: Union[str, List[str]], second: Union[str, List[str]], language: str) -> float:
        """Calculates the similarity between two words, or two list of words, returning the best result."""
        # Converting the single lists to strings
        if isinstance(first, str): first = [first]
        if isinstance(second, str): second = [second]
        try:
            nlp = self.nlp[language]
        except KeyError:
            raise LanguageNotSupportedError("This language has no modules that support it.")
        return max([
            self._similarity(first_word=first_word, second_word=second_word, language_processing_model=nlp)
            for first_word in first
            for second_word in second
        ])
    
    def _similarity(self, first_word: str, second_word: str, language_processing_model) -> float:
        """Calculate the similarity strictly between two words, given a spacy language processing model (already loaded)."""
        return language_processing_model(first_word.lower()).similarity(language_processing_model(second_word.lower()))


class NltkNlpModel(NlpModel):
    """Concrete Nlp model utilizing the NLTK natural processing module."""

    def __init__(self, supported_languages: List[str]) -> None:
        """Initializes module with the required instances."""
        self.supported_languages = supported_languages
        nltk.download("wordnet")
        nltk.download('omw-1.4')

    def calculate_similarity(self, first: Union[str, List[str]], second: Union[str, List[str]], language: str) -> float:
        """Calculates the similarity between two words, or two list of words, returning the best result."""
        if language != "en":
            raise LanguageNotSupportedError("The given language is not supported. The NLTK NLP module only supports english.")
        if isinstance(first, str): first = [first]
        if isinstance(second, str): second = [second]
        return max([
            self._similarity(first_word=first_word, second_word=second_word)
            for first_word in first
            for second_word in second
        ])
        
    def _similarity(self, first_word: str, second_word: str) -> float:
        """Calculates the similarity between two words in english and returns te result."""
        try:
            return self._encode(first_word.lower()).wup_similarity(self._encode(second_word.lower()))
        except IndexError:
            return 0.0
            
    @staticmethod
    def _encode(word: str):
        """Returns the wordnet object for a given word. If the word is not in the english langage, raises an IndexError."""
        return nltk.corpus.wordnet.synsets(word)[0]
