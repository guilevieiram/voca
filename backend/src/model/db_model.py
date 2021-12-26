from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict
from os import environ

import psycopg2
from psycopg2.errors import UniqueViolation, InFailedSqlTransaction

from .exceptions import UserIdError, UserNotFoundError, PropertyNotValidError, ValueTypeNotValidError, UserAlreadyExistsError, ConnectionToDBRefusedError

def parse_postgresql_url(url: str) -> dict:
    """A function to parse the posgresql url into a dictionary format with the login information"""
    user_data, host_data = url.lstrip("postgres://").split("@")
    user, password = user_data.split(":")
    host_port, database = host_data.split("/")
    host, port = host_port.split(":")
    return {
        "user": user, "password": password, "host": host, "port": int(port), "database": database
    }

def construct_and_query(properties: Dict[str, Union[str, int]]) -> str:
    encapsulate = lambda value: f"'{value}'"
    return " AND ".join([
        f"{property} = {value if type(value) is int else encapsulate(value)}" for property, value in properties.items()
    ])


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

    @abstractmethod
    def add_words(self, user_id: int, words: List[str]) -> None:
        """Adds a list of words in the words table in the database"""
        pass

    @abstractmethod
    def get_words(self, user_id: int) -> List[str]:
        """Gets the list of words from a user in the relevance order"""
        pass

    @abstractmethod
    def get_word_and_user_info(self, word_id: int) -> dict:
        """Gets all relevant info from a word and its user given the word ID."""
        return {
            "user": {
                "name": ...,
                "email": ...,
                "photo": ...,
                "language": ...
            },
            "word": {
                "id": ...,
                "word": ...,
                "score": ...,
                "active": ...
            }
        }

class PostgresqlDataBaseModel(DataBaseModel):
    """Data base model that is implemented using local variables to store data. Mostly to test purposes"""

    def __init__(self) -> None:
        """Initializes the data base tables as local lists"""
        self.url = environ.get("VOCA_DATABASE_URL")
        self.connection: psycopg2.connect
        self.connect()
        self.user_table_columns = ["user_name", "user_email", "user_password", "user_language", "user_photo"]

    def connect (self) -> None:
        """Method to be called to connect with the database"""
        try:
            self.connection: psycopg2.connect = psycopg2.connect(
                **parse_postgresql_url(url=self.url)
            )
            self.connection.commit()
        except Exception as e:
            raise ConnectionToDBRefusedError("Connection to the db could not be made.")

    def close_connection(self) -> None:
        """Closes connection with the database"""
        print("Closing connection with database.")
        self.connection.close()

    def add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> None: 
        """Adds a user to the database"""
        sql = f"""
        INSERT INTO app_users (user_name, user_email, user_password, user_language, user_photo)
        VALUES ('{user_name}', '{user_email}', '{user_password}', '{user_language}', '{user_photo}')
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
            self.connection.commit()
        except UniqueViolation:
            self._rollback()
            raise UserAlreadyExistsError("This email is already in use.")

    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the database"""
        sql = f"""
        DELETE FROM app_users
        WHERE id = {user_id}
        RETURNING id;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            user = cursor.fetchone()
        self.connection.commit()
        if not user:
            raise UserIdError("The required user cannot be found in the database.")

    def find_user(self, properties: Dict[str, str]) -> int:
        """Finds a user in the database"""
        if any(property not in self.user_table_columns for property in properties.keys()):
            raise PropertyNotValidError("A required property is not valid.")
        if any(type(value) is not str for value in properties.values()):
            raise ValueTypeNotValidError("A value type is not supported for this property.")
        query: str = construct_and_query(properties=properties)
        sql = f"""
        SELECT id FROM app_users
        WHERE {query}
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        if result is None:
            raise UserNotFoundError("No user was found with that property.") 
        return result[0]

    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates user in the database"""
        if property not in self.user_table_columns:
            raise PropertyNotValidError("A required property is not valid.")
        if type(value) is not str:
            raise ValueTypeNotValidError("A value type is not supported for this property.")
        sql = f"""
        UPDATE app_users
        SET {construct_and_query(properties={property: value})}
        WHERE id = {user_id}
        RETURNING id;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            user = cursor.fetchone()
        self.connection.commit()
        if user is None:
            raise UserIdError("The required user cannot be found in the database.")

    def get_user(self, user_id: int) -> dict:
        """Gets a user non-sensible info from the database and returns in the form of a dictionary."""
        sql = f"""
        SELECT user_name, user_email, user_photo, user_language
        FROM app_users
        WHERE id = {user_id}
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        if result is None:
            raise UserIdError("The requires user cannot be found in the database.")
        return {
            "user_name": result[0],
            "user_email": result[1],
            "user_photo": result[2],
            "user_language": result[3]
        }
    
    def _rollback(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("ROLLBACK")
        self.connection.commit()


class LocalDataBaseModel(DataBaseModel):
    """Data base model that is implemented using local variables to store data. Mostly to test purposes"""

    def __init__(self) -> None:
        """Initializes the data base tables as local lists"""
        self.connection: bool = True
        self.users: List[dict] = [{
            "user_name": "test",
            "user_email": "test@gmail.com",
            "user_language": "Testuguese",
            "user_password": "pass1234",
            "user_photo": "ph.com",
        }]
        self.words: List[dict] = [{
            "word": "Cup",
            "score": 20,
            "active": True,
            "user_id": 0
        }]

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

    def add_words(self, user_id: int, words: List[str]) -> None:
        """Adds a list of words in the words table in the database"""
        print(f"Adding words in the DB for the user with {user_id=}")
        for word in words:
            self.words.append({
                "word": word,
                "score": 10,
                "active": True,
                "user_id": user_id
            })

    def get_words(self, user_id: int) -> List[str]:
        """Gets the list of words from a user in the relevance order"""
        print(f"Getting all words for the user with {user_id=}")
        return [
            word
            for word in self.word
            if word.get("user_id") == user_id
        ]

    def get_word_and_user_info(self, word_id: int) -> dict:
        """Gets all relevant info from a word and its user given the word ID."""
        user_id: int = self.words[word_id].get("user_id")
        user: dict = self.users[user_id]
        word: dict = self.words[word_id]
        return {
            "user": {
                "name": user.get("user_name"),
                "email": user.get("user_email"),
                "photo": user.get("user_photo"),
                "language": user.get("user_language")
            },
            "word": {
                "id": word.get("id"),
                "word": word.get("word"),
                "score": word.get("score"),
                "active": word.get("active")
            }
        }
