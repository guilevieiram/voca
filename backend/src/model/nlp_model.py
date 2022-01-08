from abc import ABC, abstractmethod
from typing import Dict

import spacy

class NlpModel(ABC):
    """Abstract model class to handle Natural Language Processing related tasks."""

    @abstractmethod
    def calculate_similarity(self, first_word: str, second_word: str, language: str) -> float:
        """Calculates the similarity between two words."""
        pass


class DummyNlpModel(NlpModel):
    """Dummy model class to handle Natural Language Processing related tasks."""

    def calculate_similarity(self, first_word: str, second_word: str, language: str) -> float:
        """Calculates the similarity between two words."""
        return 0.98


class SpacyNlpModel(NlpModel):
    """Concrete model class to handle Natural Language Processing related tasks implemented using Spacy."""

    languages_models_mapping: Dict[str, str] = {
        "en": "en_core_web_md",
        "fr": "fr_core_news_md",
        "ru": "ru_core_news_md",
        "pt": "pt_core_news_md",
        "zh-CN": "zh_core_web_md"
    }
    
    def __init__(self) -> None:
        """Initializer to import the necessary spacy models."""
        # self.nlp = spacy.load("en_core_web_md")
        self.nlp = spacy.load("fr_core_news_md")


    def calculate_similarity(self, first_word: str, second_word: str, language: str) -> float:
        """Calculates the similarity between two words."""
        first_token = self.nlp(first_word)
        second_token = self.nlp(second_word)
        return first_token.similarity(second_token)

if __name__ == "__main__":
    n = SpacyNlpModel()
    score = n.calculate_similarity("soleil", "ciel", "en")
    print(score)