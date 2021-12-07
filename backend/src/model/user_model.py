from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union, Tuple

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    language: str 
    photo_url: str = ""
    

class UserModel(ABC):
    """Model in charge of doing all the user related calls and logic"""

    @abstractmethod
    def add_user(self, user: User) -> None:
        """Adds a given user to the data base and returns a status object"""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the data base and returns a status object"""
        pass

    @abstractmethod
    def find_user(self, property: str, value: Union[int, str]) -> User:
        """Finds a user in the data base and returns the status of the operation and the relative user object"""
        pass

    @abstractmethod
    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates a user in the data base given the user_id and returns the status of the operation """
        pass