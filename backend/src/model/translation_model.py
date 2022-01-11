from abc import ABC, abstractmethod
from typing import Callable, Union, List, Callable

import googletrans
import deep_translator

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
        self.translator: googletrans.Translator = googletrans.Translator()

    def translate(self, to_language: str, word: str, all_translations: bool = False) -> Union[str, List[str]]:
        """Translates word from detected language to to_language, returning the translated word"""
        try:
            translation: str = self.translator.translate(word, dest=to_language).text
            return translation if not all_translations else [translation]
        except ValueError:
            raise LanguageNotSupportedError("The desired language is not supported.")


class LingueeTranslationModel(TranslationModel):
    """Linguee translation model (with help from a google model to detect languages) to handle translations."""

    def __init__(self) -> None:
        """Initiates all the models possible to make the api call the fastest."""
        self.detector: Callable[[str], str] = googletrans.Translator().detect
        self.translator = deep_translator.LingueeTranslator

    def translate(self, to_language: str, word: str, all_translations: bool = False) -> Union[str, List[str]]:
        """Translates word from detected language to to_language, returning the translated word"""
        try:
            detected_language: str = self.detector(word)
            return self.translator(source=detected_language).translate(word, return_all=all_translations)
        except deep_translator.exceptions.LanguageNotSupportedException:
            raise LanguageNotSupportedError("The desired language is not supported.")