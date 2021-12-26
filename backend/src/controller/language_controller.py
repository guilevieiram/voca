from abc import abstractmethod
from typing import List

from .sub_controller import Resource, SubController, router
from src.model import NlpModel, TranslationModel, WordsModel
from src.model import WordInfo


class LanguageController(SubController):
    """Abstract controller responsible for defining the endpoints of the language related tasks of the api."""

    nlp_model: NlpModel
    translation_model: TranslationModel
    words_model: WordsModel

    @router(endpoint="")
    @abstractmethod
    def res_add_words(self, user_id: int, words: List[str]) -> dict:
        """Adds a list of words in the database for a given user located by its ID. Returns the api response dict/json."""
        pass

    @router(endpoint="")
    @abstractmethod
    def res_get_words_from_user(self, user_id: int) -> dict:
        """Gets the list of words from an user sorted by relevance, along with the words ids. Returns the api response dict/json."""
        pass

    @router(endpoint="")
    @abstractmethod
    def res_calculate_score(self, word_id: int, word: str) -> dict:
        """Calculates the similarity score between the user inputed word and the given word in the DB located by its ID. Returns the api response."""
        pass

# The implementation lacks error handling
class MyLanguageController(LanguageController):
    """Concrete controller responsible for defining the endpoints of the language related tasks of the api."""

    def __init__(self, nlp_model: NlpModel, translation_model: TranslationModel, words_model: WordsModel) -> None:
        """Initializes the controller with all the needed initialized models."""
        self.nlp_model: NlpModel = nlp_model
        self.translation_model: TranslationModel = translation_model
        self.words_model: WordsModel = words_model

    @router(endpoint="language/add_words")
    def res_add_words(self, user_id: int, words: List[str]) -> dict:
        """Adds a list of words in the database for a given user located by its ID. Returns the api response dict/json."""
        self.words_model.add_words(user_id=user_id, words=words) 
        return {
            "code": 1,
            "message": "Words added successfully."
        }

    @router(endpoint="language/get_words")
    def res_get_words_from_user(self, user_id: int) -> dict:
        """Gets the list of words from an user sorted by relevance, along with the words ids. Returns the api response dict/json."""
        words: List[str] = self.words_model.get_words_from_user(user_id=user_id)
        return {
            "code": 1,
            "message": "Words fetched successfully.",
            "words": words
        }

    # can be redesigned to take words and languages from frontend (will need more testing and confirmation)
    @router(endpoint="language/score")
    def res_calculate_score(self, word_id: int, word: str) -> dict:
        """Calculates the similarity score between the user inputed word and the given word in the DB located by its ID. Returns the api response."""
        word_info: WordInfo = self.words_model.get_word_and_language(word_id=word_id)
        translated_word: str = self.translation_model.translate(
            to_language=word_info.language,
            word=word_info.word
        )
        similarity_score = self.nlp_model.calculate_similarity(
            first_word=word,
            second_word=translated_word,
            language=language
        )
        return {
            "code": 1,
            "message": "Score calculated with success.",
            "score": similarity_score
        }