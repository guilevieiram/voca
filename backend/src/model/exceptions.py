class UserNotFoundError(Exception):
    """Exception to be raised when used cannot be found in the DB"""
    pass

class DatabaseServerError(Exception):
    """General exception to be thrown when any problem in connecting with the DB happens"""
    pass

class ProperyNotValidError(Exception):
    """Excepntion to be thrown when a user property is not valid"""
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