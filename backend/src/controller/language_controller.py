from abc import abstractmethod
from typing import List

from .sub_controller import Resource, SubController, router


class LanguageController(SubController):
    """Controller responsible for defining the endpoints of the language related tasks of the api."""

    @router("")
    @abstractmethod
    def res_add_words(self, user_id: int, words: List[str]) -> dict:
        """Adds a list of words in the database for a given user located by its ID. Returns the api response dict/json."""
        pass

    @router("")
    @abstractmethod
    def res_get_words_from_user(self, user_id: int) -> dict:
        """Gets the list of words from an user sorted by relevance, along with the words ids. Returns the api response dict/json."""
        pass

    @router("")
    @abstractmethod
    def res_calculate_score(self, word_id: int, word: str) -> dict:
        """Calculates the similarity score between the user inputed word and the given word in the DB located by its ID. Returns the api response."""
        pass
