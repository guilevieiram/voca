from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict
from os import environ

import psycopg2

from .exceptions import UserIdError, UserNotFoundError, PropertyNotValidError, ValueTypeNotValidError, UserAlreadyExistsError

def parse_postgresql_url(url: str) -> dict:
    """A function to parse the posgresql url into a dictionary format with the login information"""
    user_data, host_data = url.lstrip("postgres://").split("@")
    user, password = user_data.split(":")
    host_port, database = host_data.split("/")
    host, port = host_port.split(":")
    return {
        "user": user, "password": password, "host": host, "port": int(port), "database": database
    }

class DataBaseModel(ABC):
    """Data base abstract model responsible for connecting and sending requests to the database."""

    @abstractmethod
    def connect (self) -> None:
        """Method to be called to connect with the database"""
        pass

    @abstractmethod
    def close_connection(self) -> None:
        """Closes connection with the database"""
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
    def find_user(self, properties: Dict[str, str]) -> int:
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
            "user_photo": ...,
            "user_language": ...
        }


class PostgresqlDataBaseModel(DataBaseModel):
    """Data base model that is implemented using local variables to store data. Mostly to test purposes"""

    def __init__(self, db_name: str = "local") -> None:
        """Initializes the data base tables as local lists"""
        self.url = environ.get("VOCA_DATABASE_URL")
        self.connect()

    def connect (self) -> None:
        """Method to be called to connect with the database"""
        print("Connecting to database.")
        self.connection: psycopg2.connect = psycopg2.connect(
            **parse_postgresql_url(url=self.url)
        )
        self.connection.commit()
        print("Connected to database.")

    def close_connection(self) -> None:
        """Closes connection with the database"""
        print("Closing connection with database.")
        self.connection.close()

    def add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> None: 
        """Adds a user to the database"""
        sql = f"""
        INSERT INTO app_users (name, email, password, language, photo_url)
        VALUES ('{user_name}', '{user_email}', '{user_password}', '{user_language}', '{user_photo}')
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the database"""
        sql = f"""
        DELETE FROM app_users
        WHERE id = {user_id}
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def find_user(self, properties: Dict[str, str]) -> int:
        """Finds a user in the database"""
        query: str = " AND ".join([
            f" {property} = '{value}' " for property, value in properties.items()
        ])
        sql = f"""
        SELECT id FROM app_users
        WHERE {query}
        """
        with self.connection.cursor() as cursor:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            result, = cursor.fetchone()
        return result

    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates user in the database"""
        sql = f"""
        UPDATE app_users
        SET {property} = '{value}'
        WHERE id = {user_id}
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def get_user(self, user_id: int) -> dict:
        """Gets a user non-sensible info from the database and returns in the form of a dictionary."""
        sql = f"""
        SELECT name, email, photo_url, language
        FROM app_users
        WHERE id = {user_id}
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        return {
            "user_name": result[0],
            "user_email": result[1],
            "user_photo": result[2],
            "user_language": result[3]
        }


class LocalDataBaseModel(DataBaseModel):
    """Data base model that is implemented using local variables to store data. Mostly to test purposes"""

    def __init__(self, db_name: str = "local") -> None:
        """Initializes the data base tables as local lists"""
        self.connection: bool = True
        self.users: List[dict] = [{
            "user_name": "test",
            "user_email": "test@gmail.com",
            "user_language": "Testuguese",
            "user_password": "pass1234",
            "user_photo": "ph.com",
        }]
        self.words: List[dict] = []

    def connect (self) -> None:
        """Method to be called to connect with the database"""
        if not self.connection:
            raise ConnectionToDBRefusedError("Connection to the db could not be made.")
            
        print("Connection made!")

    def close_connection(self) -> None:
        """Closes connection with the database"""
        print("Connection closed.")

    def add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> None: 
        """Adds a user to the database"""
        if any([user.get("user_email") == user_email for user in self.users]):
            raise UserAlreadyExistsError("This email is already in use.")
        self.users.append({
            "user_name": user_name,
            "user_email": user_email,
            "user_language": user_language,
            "user_password": user_password,
            "user_photo": user_photo,
        })

    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the database"""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")

        self.users[user_id] = None

    def find_user(self, properties: Dict[str, str]) -> int:
        """Finds a user in the database"""
        if any([property not in self.users[0].keys() for property in properties.keys()]):
            raise PropertyNotValidError("A required property is not valid.")
        if any([type(value) is not str for value in properties.values()]):
            raise ValueTypeNotValidError("A value type is not supported for this property.")

        user_matches: List[int] =[
            index for index, user in enumerate(self.users) 
            if all([
                user.get(property) == value for property, value in properties.items()
            ])
        ]

        if not user_matches:
            raise UserNotFoundError("No user was found with that property.")
        return user_matches[0]

    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates user in the database"""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")
        if not property in self.users[0].keys():
            raise PropertyNotValidError("The required property is not valid.")
        if type(value) is not str:
            raise ValueTypeNotValidError("The value type is not supported for this property.")
        
        self.users[user_id][property] = value

    def get_user(self, user_id: int) -> dict:
        """Gets a user non-sensible info from the database and returns in the form of a dictionary."""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")

        user = self.users[user_id]
        return {
            "user_name": user.get("user_name"),
            "user_email": user.get("user_email"),
            "user_photo": user.get("user_photo"),
            "user_language": user.get("user_language")
        }