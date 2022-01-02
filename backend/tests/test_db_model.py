from unittest import TestCase, mock
from typing import List

from src.model import LocalDataBaseModel, PostgresqlDataBaseModel
from src.model.exceptions import UserIdError, PropertyNotValidError, UserNotFoundError, ValueTypeNotValidError, UserAlreadyExistsError, ConnectionToDBRefusedError, WordDoesNotExistError

from src.model.db_model import parse_postgresql_url, construct_and_query, UniqueViolation


class PostgresqlDataBaseModelTestCase(TestCase):

    def setUp(self):
        patcher = mock.patch('src.model.db_model.psycopg2.connect')
        self.connect = patcher.start()
        self.addCleanup(patcher.stop)

        self.connect.commit.return_value = None
        self.cursor = self.connect.return_value.cursor.return_value.__enter__.return_value

        self.db_model = PostgresqlDataBaseModel()

    def test_url_parsing(self):
        result = parse_postgresql_url(
            "postgres://username:password@asd-10-10-100-100-100.computer-1.amazonaws.com:5000/databasename"
        )
        self.assertEqual(
            result,
            {
                "user": "username",
                "password": "password",
                "host": "asd-10-10-100-100-100.computer-1.amazonaws.com",
                "port": 5000,
                "database": "databasename"
            }    
        )

    def test_construct_and_query(self):
        self.assertEqual(
            construct_and_query(properties={
                "name": "Guile",
                "email": "gui@gmail.com",
                "age": 10
            }),
            "name = 'Guile' AND email = 'gui@gmail.com' AND age = 10"
        )

    def test_connection_handling(self):
        self.connect.side_effect = Exception("ops...")
        self.assertRaises(
            ConnectionToDBRefusedError,
            self.db_model.connect
        )

    def test_add_user(self):
        self.cursor.execute.side_effect = UniqueViolation("ops..")
        patcher = mock.patch('src.model.db_model.PostgresqlDataBaseModel._rollback')
        self._rollback = patcher.start()
        self._rollback.return_value = None
        self.assertRaises(
            UserAlreadyExistsError,
            self.db_model.add_user,
            user_name="Guile",
            user_email="guile@gmail.com",
            user_password="senha123",
            user_language="french"
        )
        patcher.stop()

    def test_delete_user(self):
        self.cursor.fetchone.return_value = None
        self.assertRaises(
            UserIdError,
            self.db_model.delete_user,
            user_id=1
        )

    def test_find_user_property_not_valid(self):
        self.assertRaises(
            PropertyNotValidError, 
            self.db_model.find_user,
            properties={
                "surname": "Guile"
            }
        )
    
    def test_find_user_value_type_not_valid(self):
        self.assertRaises(
            ValueTypeNotValidError,
            self.db_model.find_user,
            properties={
                "user_name": 12
            }
        )
    
    def test_find_user_no_matches(self):
        self.cursor.fetchone.return_value = None
        self.assertRaises(
            UserNotFoundError,
            self.db_model.find_user,
            properties={
                "user_name": "Guile"
            }
        )
    
    def test_update_user_property_not_valid(self):
        self.assertRaises(
            PropertyNotValidError, 
            self.db_model.update_user,
            user_id=10,
            property="surname",
            value="Vieira"
        )

    def test_update_user_value_type_not_valid(self):
        self.assertRaises(
            ValueTypeNotValidError,
            self.db_model.update_user,
            user_id=10,
            property="user_name",
            value=10
        )
    
    def test_update_user_no_matches(self):
        self.cursor.fetchone.return_value = None
        self.assertRaises(
            UserIdError,
            self.db_model.update_user,
            user_id=10,
            property="user_name",
            value="Guile"
        )
    
    def test_get_user_no_matches(self):
        self.cursor.fetchone.return_value = None
        self.assertRaises(
            UserIdError,
            self.db_model.get_user,
            user_id=10
        )
    
    def test_add_words(self):
        self.assertIsNone(
            self.db_model.add_words(
                user_id=1,
                words=["House", "Plant"]
            )
        )
    
    def test_add_words_wrong_type(self):
        self.assertRaises(
            TypeError,
            self.db_model.add_words,
            0,
            ["House", 3]
        )
    
    def test_add_words_user_not_exists(self):
        self.cursor.fetchone.return_value = None
        self.assertRaises(
            UserIdError,
            self.db_model.add_words,
            10,
            ["House", "Horse"]
        )
    
    def test_get_words(self):
        self.cursor.fetchall.return_value = [
            ("House", ), ("Plant", )
        ]
        self.assertEqual(
            self.db_model.get_words(user_id=1),
            ["House", "Plant"]
        )

    def test_get_words_user_not_exists(self):
        self.cursor.fetchone.return_value = None
        self.assertRaises(
            UserIdError,
            self.db_model.get_words,
            user_id=10
        )
    
    def test_get_word_and_user_info(self):
        self.cursor.fetchone.return_value = (1, "Test", "test@gmail.com", "ph.com", "English", 2, "Plant", 20, True)
        self.assertEqual(
            self.db_model.get_word_and_user_info(word_id=2),
            {
                "user": {
                    "id": 1,
                    "name": "Test",
                    "email": "test@gmail.com",
                    "photo": "ph.com",
                    "language": "English"
                },
                "word": {
                    "id": 2,
                    "word": "Plant",
                    "score": 20,
                    "active": True
                }
            }
        )

    def test_get_word_and_user_info_word_not_exists(self):
        self.cursor.fetchone.return_value = None
        self.assertRaises(
            WordDoesNotExistError,
            self.db_model.get_word_and_user_info,
            word_id=100
        )

    

class LocalDbModelTestCase(TestCase):

    def setUp(self):
        self.database = LocalDataBaseModel()

    def test_add_user(self):
        self.database.add_user(
            user_name ="guilherme",
            user_email="guilhermevmanhaes@gmail.com",
            user_language="French",
            user_password="shittypass",
            user_photo="https://photo.com"
        )
        self.assertEqual(
            self.database.users[1], 
            {
                "user_name": "guilherme",
                "user_email": "guilhermevmanhaes@gmail.com",
                "user_language": "French",
                "user_password": "shittypass",
                "user_photo":"https://photo.com"
            }
        )

    def test_add_user_already_exists(self):
        self.assertRaises(
            UserAlreadyExistsError,
            self.database.add_user,
            user_name="Guile",
            user_email="test@gmail.com",
            user_password="senha1234",
            user_language="Portuguese"
        )
    
    def test_delete_user(self):
        self.database.delete_user(user_id = 0)
        self.assertIsNone(self.database.users[0])

    def test_delete_user_not_fount(self):
        self.assertRaises(
            UserIdError,
            self.database.delete_user,
            user_id=10
        )
    
    def test_find_user(self):
        user_id = self.database.find_user(properties={
            "user_name": "test"
        })
        self.assertEqual(user_id, 0)
        user_id = self.database.find_user(properties={
            "user_email": "test@gmail.com",
            "user_password": "pass1234"
        })

    def test_find_user_property_not_valid(self):
        self.assertRaises(
            PropertyNotValidError,
            self.database.find_user,
            properties={
                "user_surname": "asdf"
            }
        )

    def test_find_user_value_type_not_valid(self):
        self.assertRaises(
            ValueTypeNotValidError,
            self.database.find_user,
            properties={
                "user_name": 12
            }
        )
    
    def test_find_user_no_matches(self):
        self.assertRaises(
            UserNotFoundError,
            self.database.find_user,
            properties={
                "user_email": "email_not_existant@gmail.com"
            }
        )

    def  test_update_user(self):
        self.database.update_user(
            user_id=0,
            property="user_email",
            value="google.gmail.com"
        )
        self.assertEqual(self.database.users[0]["user_email"], "google.gmail.com")

    def test_update_user_no_matches(self):
        self.assertRaises(
            UserIdError,
            self.database.update_user,
            user_id=10,
            property="user_name",
            value="carlos"
        )
        self.database.users[0] = None
        self.assertRaises(
            UserIdError,
            self.database.update_user,
            user_id=0,
            property="user_name",
            value="Carlos"
        )

    def test_update_user_property_not_valid(self):
        self.assertRaises(
            PropertyNotValidError,
            self.database.update_user,
            user_id=0,
            property="user_surname",
            value="Martins"
        )

    def test_update_user_value_type_not_valid(self):
        self.assertRaises(
            ValueTypeNotValidError,
            self.database.update_user,
            user_id=0,
            property="user_name",
            value=12
        )

    def test_get_user(self):
        user = self.database.get_user(user_id=0)
        self.assertEqual(
            user, 
            {
                "user_name": "test",
                "user_email": "test@gmail.com",
                "user_photo": "ph.com",
                "user_language": "Testuguese"
            }
        )

    def test_get_user_no_matches(self):
        self.assertRaises(
            UserIdError,
            self.database.get_user,
            user_id=10
        )
        self.database.users[0] = None
        self.assertRaises(
            UserIdError,
            self.database.get_user,
            user_id=0
        )
    
    def test_add_words(self):
        self.database.add_words(
            user_id=0,
            words=["word1", "word2"]
        )
        self.assertEqual(
            self.database.words[1].get("word"),
            "word1"
        )
        self.assertEqual(
            self.database.words[2].get("word"),
            "word2"
        )

    def test_add_words_wrong_type(self):
        self.assertRaises(
            TypeError,
            self.database.add_words,
            0,
            ["House", 3]
        )
    
    def test_add_words_user_not_exists(self):
        self.assertRaises(
            UserIdError,
            self.database.add_words,
            10,
            ["House", "Horse"]
        )
    
    def test_get_words(self):
        self.database.words.append({
            "word": "House",
            "score": 5,
            "active": True,
            "user_id": 0
        })
        self.assertEqual(
            self.database.get_words(user_id=0),
            ["House", "Cup"]
        )

    def test_get_words_actives(self):
        self.database.words.append({
            "word": "House",
            "score": 5,
            "active": False,
            "user_id": 0
        })
        self.assertEqual(
            self.database.get_words(user_id=0),
            ["Cup"]
        )

    def test_get_words_same_user(self):
        self.database.users.append({
            "user_name": "test2",
            "user_email": "test2@gmail.com",
            "user_language": "English",
            "user_password": "ssap",
            "user_photo": "google.com"
        })
        self.database.words.append({
            "word": "House",
            "score": 5,
            "active": True,
            "user_id": 1
        })
        self.assertEqual(
            self.database.get_words(user_id=0),
            ["Cup"]
        )

    def test_get_words_user_not_exists(self):
        self.assertRaises(
            UserIdError,
            self.database.get_words,
            10
        )  
    
    def test_get_word_and_user_info(self):
        self.assertEqual(
            self.database.get_word_and_user_info(word_id=0),
            {
                "user": {
                    "id": 0,
                    "name": "test",
                    "email": "test@gmail.com",
                    "language": "Testuguese",
                    "photo": "ph.com"
                },
                "word": {
                    "id": 0,
                    "word": "Cup",
                    "score": 10,
                    "active": True
                }
            }
        )
    
    def test_get_word_and_user_info_word_not_exists(self):
        self.assertRaises(
            WordDoesNotExistError,
            self.database.get_word_and_user_info,
            10
        )






