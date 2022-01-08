"""
This module is responsible for creating the aplication controller, aka the api endpoint.
This is the heard of the application that will coordenate the requests and delegate
tasks to the models.
"""
from .main_controller import MainController, FlaskController, TerminalController
from .user_controller import UserController, DummyUserController, MyUserController
from .language_controller import LanguageController, MyLanguageController, DummyLanguageController