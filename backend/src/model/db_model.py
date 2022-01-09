from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict, Any
from os import environ

import psycopg2
from psycopg2.errors import UniqueViolation, InFailedSqlTransaction

from .exceptions import UserIdError, UserNotFoundError, PropertyNotValidError, ValueTypeNotValidError, UserAlreadyExistsError, ConnectionToDBRefusedError, WordDoesNotExistError

def parse_postgresql_url(url: str) -> dict:
    """A function to parse the posgresql url into a dictionary format with the login information"""
    user_data, host_data = url.lstrip("postgres://").split("@")
    user, password = user_data.split(":")
    host_port, database = host_data.split("/")
    host, port = host_port.split(":")
    return {
        "user": user, "password": password, "host": host, "port": int(port), "database": database
    }

def encapsulate(string: str) -> str:
    return f"'{string}'"

def construct_and_query(properties: Dict[str, Union[str, int]]) -> str:
    return " AND ".join([
        f"{property} = {value if type(value) is int else encapsulate(value)}" 
        for property, value in properties.items()
    ])

def construct_values_query(user_id: int, words: List[str]) -> str:
   return " , ".join([
       f"({encapsulate(string=word)}, {user_id})"
       for word in words
   ])


class DataBaseModel(ABC):
    """Data base abstract model responsible for connecting and sending requests to the database."""

    @abstractmethod
    def connect (self) -> None:
        """Method to be called to connect with the database"""

    @abstractmethod
    def close_connection(self) -> None:
        """Closes connection with the database"""

    @abstractmethod
    def add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> None: 
        """Adds a user to the database"""

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Deletes a user from the database"""

    @abstractmethod
    def find_user(self, properties: Dict[str, str]) -> int:
        """Finds a user in the database"""

    @abstractmethod
    def update_user(self, user_id: int, property: str, value: Union[int, str]) -> None: 
        """Updates user in the database"""

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

    @abstractmethod
    def get_words(self, user_id: int) -> List[str]:
        """Gets the list of words from a user in the relevance order"""

    @abstractmethod
    def get_word_and_user_info(self, word_id: int) -> dict:
        """Gets all relevant info from a word and its user given the word ID."""
        return {
            "user": {
                "id": ...,
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
    
    @abstractmethod
    def update_word_score(self, word_id: int, score: int) -> None:
        """Updates the given word score to the given value in the database."""


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

    def add_words(self, user_id: int, words: List[str]) -> None:
        """Adds a list of words in the words table in the database"""
        if any(not isinstance(word, str) for word in words):
            raise TypeError("The list contains items of type not string.")
        self._check_user_exitst(user_id=user_id)

        sql = f"""
        INSERT INTO app_words (word, user_id)
        VALUES {construct_values_query(user_id=user_id, words=words)};
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def get_words(self, user_id: int) -> List[str]:
        """Gets the list of words from a user in the relevance order"""
        sql = f"""
        SELECT word FROM app_words
        WHERE user_id = {user_id}
        AND active = true
        ORDER BY score;
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        self._check_user_exitst(user_id=user_id)
        return [word for word, in results]

    def get_word_and_user_info(self, word_id: int) -> dict:
        """Gets all relevant info from a word and its user given the word ID."""
        sql = f"""
        SELECT 
        u.id user_id, u.user_name,  u.user_email, u.user_photo, u.user_language,
        w.id word_id, w.word, w.score, w.active
        FROM app_users u, app_words w
        WHERE w.user_id = u.id 
        AND w.id = {word_id};
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchone()
        if results is None:
            raise WordDoesNotExistError("The required word could not be found in the database.")
        user_id, user_name, user_email, user_photo, user_language, word_id, word_word, word_score, word_active = results
        return {
            "user": {
                "id": user_id,
                "name": user_name,
                "email": user_email,
                "photo": user_photo,
                "language": user_language
            },
            "word": {
                "id": word_id,
                "word": word_word,
                "score": word_score,
                "active": word_active
            }
        }
    
    def _rollback(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute("ROLLBACK")
        self.connection.commit()
    
    def _check_user_exitst(self, user_id: int) -> None:
        "Checks if the user exists by its id by contacting the database with a simple query."
        sql = f"""SELECT id FROM app_users WHERE id = {user_id};"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        if result is None:
            raise UserIdError("The required user cannot be found in the database.")



class LocalDataBaseModel(DataBaseModel):
    """Data base model that is implemented using local variables to store data. Mostly to test purposes"""

    def __init__(self) -> None:
        """Initializes the data base tables as local lists"""
        self.connection: bool = True
        self.users: List[dict] = [{
            "user_name": "test",
            "user_email": "test@gmail.com",
            "user_language": "en",
            "user_password": "pass1234",
            "user_photo": "ph.com",
        }]
        self.words: List[dict] = [{
            "word": "Cup",
            "score": 10,
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

    def add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: str) -> None: 
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
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")
        if any(not isinstance(word, str) for word in words):
            raise TypeError("The list contains items of type not string.")
        for word in words:
            self.words.append({
                "word": word,
                "score": 10,
                "active": True,
                "user_id": user_id
            })

    def get_words(self, user_id: int) -> List[str]:
        """Gets the list of words from a user in the relevance order"""
        if not user_id < len(self.users) or self.users[user_id] is None:
            raise UserIdError("The required user cannot be found in the database.")
        words: List[dict]  = [
            word
            for word in self.words
            if word.get("user_id") == user_id
            and word.get("active")
        ]
        return [word.get("word") for word in sorted(words, key = lambda word: word.get("score"))]

    def get_word_and_user_info(self, word_id: int) -> dict:
        """Gets all relevant info from a word and its user given the word ID."""
        try:
            user_id: int = self.words[word_id].get("user_id")
        except IndexError:
            raise WordDoesNotExistError("The required word could not be found in the database.")
        try:
            user: dict = self.users[user_id]
        except IndexError:
            raise UserIdError("The required user could not be found in the database.")
        word: dict = self.words[word_id]
        return {
            "user": {
                "id": user_id,
                "name": user.get("user_name"),
                "email": user.get("user_email"),
                "photo": user.get("user_photo"),
                "language": user.get("user_language")
            },
            "word": {
                "id": word_id,
                "word": word.get("word"),
                "score": word.get("score"),
                "active": word.get("active")
            }
        }

    def update_word_score(self, word_id: int, score: int) -> None:
        """Updates the given word score to the given value in the database."""
        try:
            self.words[word_id]["score"] = score
        except IndexError:
            raise WordDoesNotExistError("The required word does not exists.")
        

