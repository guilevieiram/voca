from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional, List

from .sub_controller import Resource, SubController, router, Error

from src.model import UserModel, User
from src.model.exceptions import UserNotFoundError, UserIdError, UserAlreadyExistsError, WrongPasswordError, PropertyNotValidError, ValueTypeNotValidError


class UserController(SubController):
    """
    UserController abstract class responsible for defining user related resources.
    """

    @abstractmethod
    def close_connection(self) -> None:
        """Closes connections with databases"""
        pass
        
    @router(endpoint="")
    @abstractmethod
    def res_login(self, user_email: str, password: str) -> dict:
        """Logs a user in and returns the dict message with the user id (if successfull)"""
        pass

    @router(endpoint="")
    @abstractmethod
    def res_sign_up(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> dict: 
        """Add a user in the system."""
        pass
        
    @router(endpoint="")
    @abstractmethod
    def res_delete_user(self, user_id: id) -> dict: 
        """Delete a user in the system."""
        pass
        
    @router(endpoint="")
    @abstractmethod
    def res_get_user(self, user_id: int) -> dict: 
        """Find a user in the system."""
        pass
        
    @router(endpoint="")
    @abstractmethod
    def res_update_user(self, user_id: int, property: str, value: Any) -> dict: 
        """Update a user in the system."""
        pass


class DummyUserController(UserController):
    """
    UserController dummy class responsible for defining user related resources.
    """
    
    def close_connection(self) -> None:
        """Closes connections with databases"""
        print("Closing connections.")
    
    @router(endpoint="user/login")
    def res_login(self, user_email: str, password: str) -> dict:
        """Logs a user in and returns the dict message with the user id (if successfull)"""
        return {
            "code": 1,
            "message": f"User {user_email=} logged in.",
            "user_id": 0
        }

    @router(endpoint="user/signup")
    def res_sign_up(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> dict: 
        """Add a user in the system."""
        return {
            "code": 1,
            "message": f"Adding user with {user_name=}, {user_email=}, {user_password=}, {user_language=}, {user_photo=}"
        }

    @router(endpoint="user/delete")
    def res_delete_user(self, user_id: id) -> dict: 
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
            "message": f"Finding user with {property=}, {value=}"
        }

    @router(endpoint="user/update")
    def res_update_user(self, user_id: int, property: str, value: Any) -> dict: 
        """Update a user in the system."""
        return {
            "code": 1,
            "message": f"Updating user with {user_id=}, {property=}, {value=}"
        }


class MyUserController(UserController):
    """
    UserController implementation responsible for defining user related resources.
    """

    def __init__(self, user_model: UserModel):
        """Initializer that makes connection with the required user model"""
        self.user_model = user_model

    def close_connection(self) -> None:
        """Closes connections with databases"""
        self.user_model.close_connection()
        
    @router(endpoint="user/login")
    def res_login(self, user_email: str, password: str) -> dict:
        """Logs a user in and returns the dict message with the user id (if successfull)"""
        try:
            user_id: int = self.user_model.get_user_id(properties={
                "user_email": user_email,
                "user_password": password
            })
            return {
                "code": 1,
                "message": "Login successful.",
                "id": user_id
            }
        except WrongPasswordError:
            return {
                "code": Error.WRONG_PASSWORD_ERROR.value,
                "message": "Wrong password."
            }
        except Exception as e: 
            print(type(e), e)
            return {
                "code": Error.DATABASE_SERVER_ERROR.value,
                "message": "A problem occured with the database."
            }

    @router(endpoint="user/signup")
    def res_sign_up(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> dict: 
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
        except:
            return {
                "code": Error.DATABASE_SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }

    @router(endpoint="user/delete")
    def res_delete_user(self, user_id: id) -> dict: 
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
        except:
            return {
                "code": Error.DATABASE_SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }

    @router(endpoint="user/get")
    def res_get_user(self, user_id: int) -> dict: 
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
        except:
            return {
                "code": Error.DATABASE_SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }

    @router(endpoint="user/update")
    def res_update_user(self, user_id: int, property: str, value: Any) -> dict: 
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
        except:
            return {
                "code": Error.DATABASE_SERVER_ERROR.value,
                "message": "A problem occured in the database."
            }