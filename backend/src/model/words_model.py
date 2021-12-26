from abc import ABC, abstractmethod
from typing import List, Tuple
from dataclasses import dataclass

from .db_model import DataBaseModel

@dataclass
class WordInfo:
    word: str
    language: str


class WordsModel(ABC):
    """Abstract model class to handle the words related methods with the database"""

    database_model: DataBaseModel

    @abstractmethod
    def add_words(self, user_id: int, words: List[str]) -> None:
        """Adds a list of words in the DB associated with a user"""
        pass

    @abstractmethod
    def get_words_from_user(self, user_id: int) -> List[str]:
        """Fetches a list of words from the DB and returns as list in importance order"""
        pass

    @abstractmethod
    def get_word_and_language(self, word_id: int) -> WordInfo:
        """Fetches the word and language of that word given the word ID."""
        pass


class DummyWordsModel(WordsModel):
    """Dummy model class to handle the words related methods with the database"""

    def __init__(self, database_model: DataBaseModel) -> None:
        """Initializes the model with the necessary auxiliary DB model"""
        self.database_model: DataBaseModel = database_model

    def add_words(self, user_id: int, words: List[str]) -> None:
        """Adds a list of words in the DB associated with a user"""
        print(f"Adding words {','.join(words)} in the user {user_id}.")

    def get_words_from_user(self, user_id: int) -> List[str]:
        """Fetches a list of words from the DB and returns as list in importance order"""
        return ["Word1", "Word2", "Word3"]

    def get_word_and_language(self, word_id: int) -> WordInfo:
        """Fetches the word and language of that word given the word ID."""
        return WordInfo(word="Word1", language="english")


class MyWordsModel(WordsModel):
    """Concrete model class to handle the words related methods with the database"""

    def __init__(self, database_model: DataBaseModel) -> None:
        """Initializes the model with the necessary auxiliary DB model"""
        self.database_model: DataBaseModel = database_model

    def add_words(self, user_id: int, words: List[str]) -> None:
        """Adds a list of words in the DB associated with a user"""
        self.database_model.add_words(user_id=user_id, words=words)

    def get_words_from_user(self, user_id: int) -> List[str]:
        """Fetches a list of words from the DB and returns as list in importance order"""
        return self.database_model.get_words(user_id=user_id)

    def get_word_and_language(self, word_id: int) -> WordInfo:
        """Fetches the word and language of that word given the word ID."""
        infos: dict = self.database_model.get_word_and_user_info(word_id=word_id)
        return WordInfo(
            word=infos.get("word").get("word"),
            language=infos.get("user").get("language")
        )