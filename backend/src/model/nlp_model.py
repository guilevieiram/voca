from abc import ABC, abstractmethod
from typing import Dict, Any, List

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

    
    def __init__(self, supported_languages: List[str]) -> None:
        """Initializer to import the necessary spacy models."""

        languages_models_mapping: dict[str, str] = {
            "en": "en_core_web_md",
            "fr": "fr_core_news_md",
            "ru": "ru_core_news_md",
            "pt": "pt_core_news_md",
            "zh-cn": "zh_core_web_md"
        }

        self.nlp: Dict[str, Any] = {} # dictionary to encapsulate all the loaded modules
        for language in supported_languages:
            self.nlp[language] = spacy.load(languages_models_mapping[language])


    def calculate_similarity(self, first_word: str, second_word: str, language: str) -> float:
        """Calculates the similarity between two words."""
        first_token = self.nlp[language](first_word)
        second_token = self.nlp[language](second_word)
        print(f"the similarity between {first_token} and {second_token} is {first_token.similarity(second_token)}")
        return first_token.similarity(second_token)

if __name__ == "__main__":
    n = SpacyNlpModel()
    score = n.calculate_similarity("soleil", "ciel", "fr")
    print(score)