from abc import ABC, abstractmethod
from typing import List, Optional, Union


class DataBaseModel(ABC):
    """Data base abstract model responsible for connecting and sending requests to the database."""

    @abstractmethod
    def connect (self) -> None:
        """Method to be called to connect with the database"""
        pass

    @abstractmethod
    def add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> None: 
        """Adds a user to the database"""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the database"""
        pass

    @abstractmethod
    def find_user(self, property: str, value: Union[int, str]) -> int:
        """Finds a user in the database"""
        pass

    @abstractmethod
    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates user in the database"""
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> dict:
        """Gets a user non-sensible info from the database and returns in the form of a dictionary."""
        return {
            "user_name": ...,
            "user_email": ...,
            "user_photo": ...
        }

class LocalDataBase(DataBaseModel):
    """Data base model that is implemented using local variables to store data. Mostly to test purposes"""

    def __init__(self, db_name: str = "local") -> None:
        """Initializes the data base tables as local lists"""
        self.connection: bool = True
        self.users: List[dict] = [{
            "user_name": "test",
            "user_email": "test@gmail.com",
            "user_password": "pass1234",
            "user_photo": "ph.com",
        }]
        self.words: List[dict] = []

    def connect (self) -> None:
        """Method to be called to connect with the database"""
        if not self.connection:
            raise ConnectionToDBRefusedError("Connection to the db could not be made.")
        print("Connection made!")

    def add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> None: 
        """Adds a user to the database"""
        self.users.append({
            "user_name": user_name,
            "user_email": user_email,
            "user_password": user_password,
            "user_photo": user_photo,
        })

    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the database"""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")
        self.users[user_id] = None

    def find_user(self, property: str, value: Union[int, str]) -> int:
        """Finds a user in the database"""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")
        if not property in self.users[0].keys():
            raise PropertyNotValidError("The required property is not valid.")

        user_matches: List[int] = [index for index, user in enumerate(self.users) if user.get(property) == value]
        
        if not user_matches:
            raise UserNotFoundError("No user was found with that property.")
        
        return user_matches[0]

    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates user in the database"""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")
        if not property in self.users[0].keys():
            raise PropertyNotValidError("The required property is not valid.")
        self.users[user_id][property] = value

    def get_user(self, user_id: int) -> dict:
        """Gets a user non-sensible info from the database and returns in the form of a dictionary."""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")
        user = self.users[user_id]
        return {
            "user_name": user.get("user_name"),
            "user_email": user.get("user_email"),
            "user_photo": user.get("user_photo")
        }