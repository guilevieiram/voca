from enum import Enum

class Error(Enum):
    USER_NOT_FOUND_ERROR = -1
    WRONG_PASSWORD_ERROR = -2 
    DATABASE_SERVER_ERROR = -3 
    PROPERTY_NOT_VALID_ERROR = -4 
    USER_ID_ERROR = -5 
    USER_ALREADY_EXISTS_ERROR = -6
    VALUE_TYPE_NOT_VALID_ERROR = -7

