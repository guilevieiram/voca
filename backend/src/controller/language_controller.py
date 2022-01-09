from abc import abstractmethod
from typing import Callable, List, Dict
from json import load

from src.model import WordInfo 
from src.model import NlpModel, TranslationModel, WordsModel
from src.model import WordInfo
from src.model.exceptions import LanguageNotSupportedError, UserIdError, WordDoesNotExistError, TranslationApiConnectionError, TranslationNotFound, NlpCalculationError

from .sub_controller import Method, SubController, router, ResourceResponse
from .error import Error


class LanguageController(SubController):
    """Abstract controller responsible for defining the endpoints of the language related tasks of the api."""

    nlp_model: NlpModel
    translation_model: TranslationModel
    words_model: WordsModel
    supported_languages: List[Dict[str, str]]
    conversion_function: Callable[..., int] # converts float to int but python keeps sending me errors if I put float in the type annotation

    @router(endpoint="")
    @abstractmethod
    def res_add_words(self, user_id: int, words: List[str]) -> ResourceResponse:
        """Adds a list of words in the database for a given user located by its ID. Returns the api response dict/json."""

    @router(endpoint="")
    @abstractmethod
    def res_get_words_from_user(self, user_id: int) -> ResourceResponse:
        """Gets the list of words from an user sorted by relevance, along with the words ids. Returns the api response dict/json."""

    @router(endpoint="")
    @abstractmethod
    def res_calculate_score(self, word_id: int, word: str) -> ResourceResponse:
        """Calculates the similarity score between the user inputed word and the given word in the DB located by its ID. Returns the api response."""

    @router(endpoint="")
    @abstractmethod
    def res_get_supported_languages(self) -> ResourceResponse:
        """Returns the dictionary of the supported languages on user signup."""
        return {
            "code": ...,
            "message": ...,
            "languages": [
                {
                    "name": ...,
                    "flag": ...,
                    "code": ...
                }, ...
            ]
        }

class DummyLanguageController(LanguageController):
    """Dummy controller responsible for defining the endpoints of the language related tasks of the api."""

    def __init__(self, nlp_model: NlpModel, translation_model: TranslationModel, words_model: WordsModel, supported_languages: List[Dict[str, str]], conversion_function: Callable) -> None:
        """Initializes the controller with all the needed initialized models."""
        self.nlp_model: NlpModel = nlp_model
        self.translation_model: TranslationModel = translation_model
        self.words_model: WordsModel = words_model
        self.supported_languages: List[Dict[str, str]] = supported_languages
        self.conversion_function: Callable = conversion_function

    @router(endpoint="language/add_words")
    def res_add_words(self, user_id: int, words: List[str]) -> ResourceResponse:
        """Adds a list of words in the database for a given user located by its ID. Returns the api response dict/json."""
        return {
            "code": 1,
            "message": "Words added successfully."
        }

    @router(endpoint="language/get_words")
    def res_get_words_from_user(self, user_id: int) -> ResourceResponse:
        """Gets the list of words from an user sorted by relevance, along with the words ids. Returns the api response dict/json."""
        return {
            "code": Error.USER_ID_ERROR.value,
            "message": "Words fetched successfully.",
            "words": ["House", "Plant"]
        }
        
    @router(endpoint="language/score")
    def res_calculate_score(self, word_id: int, word: str) -> ResourceResponse:
        """Calculates the similarity score between the user inputed word and the given word in the DB located by its ID. Returns the api response."""
        return {
            "code": 1,
            "message": "Score calculated successfully.",
            "score": 0.78737
        }

    @router(endpoint="language/supported_languages", method=Method.GET)
    def res_get_supported_languages(self) -> ResourceResponse:
        """Returns the dictionary of the supported languages on user signup."""
        return {
            "code": 1,
            "message": "Supported languages fetched successfully.",
            "languages": self.supported_languages
        }


# The implementation user input type checking error handling
class MyLanguageController(LanguageController):
    """Concrete controller responsible for defining the endpoints of the language related tasks of the api."""

    def __init__(self, nlp_model: NlpModel, translation_model: TranslationModel, words_model: WordsModel, supported_languages: List[Dict[str, str]], conversion_function: Callable) -> None:
        """Initializes the controller with all the needed initialized models."""
        self.nlp_model: NlpModel = nlp_model
        self.translation_model: TranslationModel = translation_model
        self.words_model: WordsModel = words_model
        self.supported_languages: List[Dict[str, str]] = supported_languages
        self.conversion_function: Callable = conversion_function

    @router(endpoint="language/add_words")
    def res_add_words(self, user_id: int, words: List[str]) -> ResourceResponse:
        """Adds a list of words in the database for a given user located by its ID. Returns the api response dict/json."""
        try:
            self.words_model.add_words(user_id=user_id, words=words) 
            return {
                "code": 1,
                "message": "Words added successfully."
            }
        except UserIdError:
            return {
                "code": Error.USER_ID_ERROR.value,
                "message": "The desired user was not found in the database." 
            }
        except Exception as e:
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "An error occured in the database."
            }

    @router(endpoint="language/get_words")
    def res_get_words_from_user(self, user_id: int) -> ResourceResponse:
        """Gets the list of words from an user sorted by relevance, along with the words ids. Returns the api response dict/json."""
        try:
            words: List[str] = self.words_model.get_words_from_user(user_id=user_id)
            return {
                "code": 1,
                "message": "Words fetched successfully.",
                "words": words
            }
        except UserIdError:
            return {
                "code": Error.USER_ID_ERROR.value,
                "message": "The desired user was not found in the database."
            }
        except Exception:
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "An error occured in the database."
            }
            
    # can be redesigned to take words and languages from frontend (will need more testing and confirmation)
    @router(endpoint="language/score")
    def res_calculate_score(self, word_id: int, word: str) -> ResourceResponse:
        """Calculates the similarity score between the user inputed word and the given word in the DB located by its ID. Returns the api response."""
        try:
            word_info: WordInfo = self.words_model.get_word_and_language(word_id=word_id)
            translated_word: str = self.translation_model.translate(
                to_language=word_info.language,
                word=word
            )
            similarity_score = self.nlp_model.calculate_similarity(
                first_word=word_info.word,
                second_word=translated_word,
                language=word_info.language
            )
            self.words_model.update_word_score(
                word_id=word_id,
                score=self.conversion_function(similarity_score)
            )
            return {
                "code": 1,
                "message": "Score calculated successfully.",
                "score": similarity_score
            }
        except WordDoesNotExistError:
            return {
                "code": Error.WORD_DOES_NOT_EXISTS_ERROR.value,
                "message": "No word with the given ID could be found in the database."
            }
        except UserIdError:
            return {
                "code": Error.USER_NOT_FOUND_ERROR.value,
                "message": "The related user could not be found in the database."
            }
        except TranslationNotFound:
            return {
                "code": Error.TRANSLATION_NOT_FOUND_ERROR.value,
                "message": "The given word could not be translated."
            }
        except LanguageNotSupportedError:
            return {
                "code": Error.LANGUAGE_NOT_SUPPORTED_ERROR.value,
                "message": "The desired language is not supported."
            }
        except TranslationApiConnectionError:
            return {
                "code": Error.TRANSLATION_API_CONNECTION_ERROR.value,
                "message": "Connection with the translator could not be made."
            }
        except NlpCalculationError:
            return {
                "code": Error.NLP_CALCULATION_ERROR.value,
                "message": "The NLP model could not calculate your request."
            }
        except Exception as e:
            print(type(e), e)
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "An error occured in the database."
            }

    @router(endpoint="language/supported_languages", method=Method.GET)
    def res_get_supported_languages(self) -> ResourceResponse:
        """Returns the dictionary of the supported languages on user signup."""
        print("called")
        if self.supported_languages is None:
            return {
                "code": Error.SUPPORTED_LANGUAGES_NOT_FOUND_ERROR,
                "message": "The list of supported languages could not be found."
            }
        return {
            "code": 1,
            "message": "Supported languages fetched successfully.",
            "languages": self.supported_languages
        }