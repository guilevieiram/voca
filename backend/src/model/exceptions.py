class UserNotFoundError(Exception):
    """Exception to be raised when used cannot be found in the DB"""
    pass

class DatabaseError(Exception):
    """General exception to be thrown when any problem in connecting with the DB happens"""
    pass

class PropertyNotValidError(Exception):
    """Excepntion to be thrown when a user property is not valid"""
    pass

class ValueTypeNotValidError(Exception):
    """Exception to be raised when the type of the value to be changed is not correct"""
    pass

class UserAlreadyExistsError(Exception):
    """Exception to be raised when the user trying to be added already exists"""
    pass

class UserIdError(Exception):
    """Exception to be thrown when a given user id is not valid (not in the db)"""
    pass

class WrongPasswordError(Exception):
    """Exception to be thrown when a given password doesnt match the user password in the db"""
    pass

class ConnectionToDBRefusedError(Exception):
    """Exception to be called when the connection with the db is refused."""
    pass

class WordDoesNotExistError(Exception):
    """Exception to be raised when a word cannot be found in the database"""
    pass

class TranslationNotFound(Exception):
    """Exception to be raised when a word cannot be translated by the api"""
    pass

class TranslationApiConnectionError(Exception):
    """Exception to be raised when the translation routine cannot be accessed"""
    pass

class NlpCalculationError(Exception):
    """Exception to be raised when the NLP algorithm cannot complete the given task."""

class LanguageNotSupportedError(Exception):
    """Exception to be raised when a not supported language is demanded."""