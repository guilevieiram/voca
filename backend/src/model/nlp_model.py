from abc import ABC, abstractmethod
from typing import Dict, Any, List

import spacy

from src.model.exceptions import LanguageNotSupportedError

class NlpModel(ABC):
    """Abstract model class to handle Natural Language Processing related tasks."""

    @abstractmethod
    def calculate_similarity(self, first_word: str, second_word: str, language: str) -> float:
        """Calculates the similarity between two words."""
        pass


class DummyNlpModel(NlpModel):
    """Dummy model class to handle Natural Language Processing related tasks."""

    def __init__(self, *args, **kwargs) -> None:
        """Dummy init method to get whatever parameters"""

    def calculate_similarity(self, first_word: str, second_word: str, language: str) -> float:
        """Calculates the similarity between two words."""
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
            self.nlp[language] = spacy.load(languages_models_mapping[language])

    def calculate_similarity(self, first_word: str, second_word: str, language: str) -> float:
        """Calculates the similarity between two words in a given language."""
        if not isinstance(first_word, str) or not isinstance(second_word, str):
            raise TypeError("The words should be passed in as strings.")

        try:
            nlp = self.nlp[language]
        except KeyError:
            raise LanguageNotSupportedError("This language has no modules that support it.")
        return nlp(first_word).similarity(nlp(second_word))