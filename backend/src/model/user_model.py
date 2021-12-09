from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union, Tuple, Optional, Dict

from .db_model import DataBaseModel
from .exceptions import UserNotFoundError, WrongPasswordError


@dataclass
class User:
    name: str
    email: str
    language: str 
    id: int = 0
    password: Optional[str] = None
    photo_url: str = ""
    

class UserModel(ABC):
    """Model in charge of doing all the user related calls and logic"""

    @abstractmethod
    def add_user(self, user: User) -> None:
        """Adds a given user to the data base."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the data base."""
        pass

    @abstractmethod
    def get_user(self, user_id) -> User:
        """Finds a user in the data base by its id and returns the user object."""
        pass

    @abstractmethod
    def get_user_id(self, properties: Dict[str, str]) -> int:
        """Gets the first found user that satisfy the property value dictionary pairs"""
        pass

    @abstractmethod
    def login_user(self, user_email: str, user_password: str) -> int:
        """Logs in a user with email and password, returning the user id if valid credentials"""
        pass

    @abstractmethod
    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates a user in the data base given the user_id and a property, value pair."""
        pass


class MyUserModel(UserModel):
    """Simple logic implementation of the user model."""

    def __init__(self, db_model: DataBaseModel) -> None:
        """Initializes connection with the data base auxiliary model"""
        self.db_model = db_model

    def add_user(self, user: User) -> None:
        """Adds a given user to the data base."""
        self.db_model.add_user(
            user_name=user.name,
            user_email=user.email,
            user_password=user.password,
            user_language=user.language
        )

    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the data base."""
        self.db_model.delete_user(user_id=user_id)

    def get_user(self, user_id: int) -> User:
        """Finds a user in the data base by the id and returns the user object."""
        user_information = self.db_model.get_user(user_id=user_id)
        return User(
            id=user_id,
            name=user_information.get("user_name"),
            email=user_information.get("user_email"),
            language=user_information.get("user_language"),
            photo_url=user_information.get("user_photo")
        )

    def get_user_id(self, properties: Dict[str, str]) -> int:
        """Gets the first found user that satisfy that property"""
        return self.db_model.find_user(properties=properties)
    
    def login_user(self, user_email: str, user_password: str) -> int:
        """Tries to log in the user returning the user id if successful"""
        try:
            return self.db_model.find_user(properties={
                "user_email": user_email,
                "user_password": user_password
            })
        except UserNotFoundError:
            raise WrongPasswordError("Given credentials do not match.")


    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates a user in the data base given the user_id and a property, value pair."""
        self.db_model.update_user(user_id=user_id, property=property, value=value)