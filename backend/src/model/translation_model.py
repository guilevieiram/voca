from abc import ABC, abstractmethod

class TranslationModel(ABC):
    """Abstract model class to handle translation of words between languages"""

    @abstractmethod
    def translate(self, to_language: str, word: str) -> str:
        """Translates word from detected language to to_language, returning the translated word"""
        pass
     

class DummyTranslationModel(TranslationModel):
    """Dummy model class to handle translation of words between languages"""

    def translate(self, to_language: str, word: str) -> str:
        """Translates word from detected language to to_language, returning the translated word"""
        return f"<{word} in {to_language}>"