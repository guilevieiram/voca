from abc import ABC, abstractmethod

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