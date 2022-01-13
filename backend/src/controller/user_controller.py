from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Any, Optional 
import logging

from .sub_controller import SubController, router, ResourceResponse
from .error import Error

from src.model import UserModel, User
from src.model.exceptions import UserNotFoundError, UserIdError, UserAlreadyExistsError, WrongPasswordError, PropertyNotValidError, ValueTypeNotValidError


class UserController(SubController):
    """UserController abstract class responsible for defining user related resources."""

    user_model: UserModel
    logger: logging.Logger

    @abstractmethod
    def close_connection(self) -> None:
        """Closes connections with databases"""
        
    @router(endpoint="user/login")
    @abstractmethod
    def res_login(self, user_email: str, password: str) -> ResourceResponse:
        """Logs a user in and returns the dict message with the user id (if successfull)"""

    @router(endpoint="user/signup")
    @abstractmethod
    def res_sign_up(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> ResourceResponse:
        """Add a user in the system."""
        
    @router(endpoint="user/delete")
    @abstractmethod
    def res_delete_user(self, user_id: id) -> ResourceResponse:
        """Delete a user in the system."""
        
    @router(endpoint="user/get")
    @abstractmethod
    def res_get_user(self, user_id: int) -> ResourceResponse:
        """Find a user in the system."""
        
    @router(endpoint="user/update")
    @abstractmethod
    def res_update_user(self, user_id: int, property: str, value: Any) -> ResourceResponse:
        """Update a user in the system."""


class DummyUserController(UserController):
    """UserController dummy class responsible for defining user related resources."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes the dummy controller with whatever args it needs"""
    
    def close_connection(self) -> None:
        """Closes connections with databases"""
        print("Closing connections.")
    
    @router(endpoint="user/login")
    def res_login(self, user_email: str, password: str) -> ResourceResponse:
        """Logs a user in and returns the dict message with the user id (if successfull)"""
        return {
            "code": 1,
            "message": f"User {user_email=} logged in.",
            "id": 0
        }

    @router(endpoint="user/signup")
    def res_sign_up(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> ResourceResponse:
        """Add a user in the system."""
        return {
            "code": 1,
            "message": f"Adding user with {user_name=}, {user_email=}, {user_password=}, {user_language=}, {user_photo=}"
        }

    @router(endpoint="user/delete")
    def res_delete_user(self, user_id: id) -> ResourceResponse:
        """Delete a user in the system."""
        return {
            "code": 1,
            "message": f"Deleting user with {user_id=}"
        }

    @router(endpoint="user/get")
    def res_get_user(self, user_id: int) -> dict: 
        """Find a user in the system."""
        return {
            "code": 1,
            "message": f"Getting user with {user_id=}"
        }

    @router(endpoint="user/update")
    def res_update_user(self, user_id: int, property: str, value: Any) -> ResourceResponse:
        """Update a user in the system."""
        return {
            "code": 1,
            "message": f"Updating user with {user_id=}, {property=}, {value=}"
        }


class MyUserController(UserController):
    """UserController implementation responsible for defining user related resources."""

    def __init__(self, user_model: UserModel, logger: logging.Logger):
        """Initializer that makes connection with the required user model"""
        self.user_model = user_model
        self.logger: logging = logger

    def close_connection(self) -> None:
        """Closes connections with databases"""
        self.user_model.close_connection()
        
    @router(endpoint="user/login")
    def res_login(self, user_email: str, password: str) -> ResourceResponse:
        """Logs a user in and returns the dict message with the user id (if successfull)"""
        try:
            user_id: int = self.user_model.login_user(
                user_email=user_email,
                user_password=password
            )
            return {
                "code": 1,
                "message": "Login successful.",
                "id": user_id
            }
        except UserNotFoundError:
            return {
                "code": Error.USER_NOT_FOUND_ERROR.value,
                "message": "This user does not exists."
            }
        except WrongPasswordError:
            return {
                "code": Error.WRONG_PASSWORD_ERROR.value,
                "message": "Wrong password."
            }
        except Exception:
            self.logger.exception("An exception occurred in the server.")
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "A problem occured with the database."
            }

    @router(endpoint="user/signup")
    def res_sign_up(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> ResourceResponse:
        """Add a user in the system."""
        try:
            self.user_model.add_user(user=User(
                name=user_name,
                email=user_email,
                language=user_language,
                password=user_password,
                photo_url=user_photo
            ))
            return {
                "code": 1,
                "message": "User added with no problem."
            }
        except UserAlreadyExistsError:
            return {
                "code": Error.USER_ALREADY_EXISTS_ERROR.value,
                "message": "This user email is already in use."
            }
        except Exception:
            self.logger.exception("An exception occurred in the server.")
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }

    @router(endpoint="user/delete")
    def res_delete_user(self, user_id: id) -> ResourceResponse:
        """Delete a user in the system."""
        try:
            self.user_model.delete_user(user_id=user_id)
            return {
                "code": 1,
                "message": "User deleted."
            }
        except UserIdError:
            return {
                "code": Error.USER_ID_ERROR.value,
                "message": "Given user id is not valid."
            }
        except Exception:
            self.logger.exception("An exception occurred in the server.")
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }

    @router(endpoint="user/get")
    def res_get_user(self, user_id: int) -> ResourceResponse:
        """Find a user in the system."""
        try:
            user_info: User = self.user_model.get_user(user_id=user_id)
            return {
                "code": 1,
                "message": "User data fetched with success.",
                "user": asdict(user_info)
            }
        except UserIdError:
            return {
                "code": Error.USER_ID_ERROR.value,
                "message": "Given user id is not valid."
            }
        except Exception:
            self.logger.exception("An exception occurred in the server.")
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }

    @router(endpoint="user/update")
    def res_update_user(self, user_id: int, property: str, value: Any) -> ResourceResponse:
        """Update a user in the system."""
        try:
            self.user_model.update_user(
                user_id=user_id,
                property=property,
                value=value
            )
            return {
                "code": 1,
                "message": "User successfully updated."
            }
        except UserIdError:
            return {
                "code": Error.USER_ID_ERROR.value,
                "message": "Given user id is not valid."
            }
        except PropertyNotValidError:
            return {
                "code": Error.PROPERTY_NOT_VALID_ERROR.value,
                "message": "The given property is not valid."
            }
        except ValueTypeNotValidError:
            return {
                "code": Error.VALUE_TYPE_NOT_VALID_ERROR.value,
                "message": "The wanted value is not from the right type."
            }
        except Exception:
            self.logger.exception("An exception occurred in the server.")
            return {
                "code": Error.SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }