from enum import Enum

class Error(Enum):
    USER_NOT_FOUND_ERROR = -1
    WRONG_PASSWORD_ERROR = -2 
    DATABASE_ERROR = -3 
    PROPERTY_NOT_VALID_ERROR = -4 
    USER_ID_ERROR = -5 
    USER_ALREADY_EXISTS_ERROR = -6
    VALUE_TYPE_NOT_VALID_ERROR = -7
    WORD_DOES_NOT_EXISTS_ERROR = -8
    TRANSLATION_NOT_FOUND_ERROR = -9
    TRANSLATION_API_CONNECTION_ERROR = -10
    NLP_CALCULATION_ERROR = -11
    SERVER_ERROR = -12
    SUPPORTED_LANGUAGES_NOT_FOUND_ERROR = -13
    LANGUAGE_NOT_SUPPORTED_ERROR = -14