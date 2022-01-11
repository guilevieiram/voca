from abc import ABC, abstractmethod
from typing import Union, List

from googletrans import Translator
from .exceptions import LanguageNotSupportedError


class TranslationModel(ABC):
    """Abstract model class to handle translation of words between languages"""

    @abstractmethod
    def translate(self, to_language: str, word: str, all_translations: bool = False) -> Union[str, List[str]]:
        """Translates word from detected language to to_language, returning the translated word"""
     

class DummyTranslationModel(TranslationModel):
    """Dummy model class to handle translation of words between languages"""

    def translate(self, to_language: str, word: str, all_translations: bool = False) -> Union[str, List[str]]:
        """Translates word from detected language to to_language, returning the translated word"""
        return f"<{word} in {to_language}>"
    

class GoogleTranslationModel(TranslationModel):
    """Google based model class to handle translation of words between languages"""

    def __init__ (self) -> None:
        """Initializes the model with the API translator object."""
        self.translator: Translator = Translator()

    def translate(self, to_language: str, word: str, all_translations: bool = False) -> Union[str, List[str]]:
        """Translates word from detected language to to_language, returning the translated word"""
        try:
            translation: str = self.translator.translate(word, dest=to_language).text
            return translation if not all_translations else [translation]
        except ValueError:
            raise LanguageNotSupportedError("The desired language is not supported.")
