from flask import Flask, request, abort
from flask_cors import CORS
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from .sub_controller import Resource, SubController 
from .user_controller import UserController


def get_parameters(parameters_names: List[str]) -> Dict[str, Any]:
    """Get parameters from the desired api call"""
    if not request.json or set(request.json.keys()) != set(parameters_names):
        abort(400)
    return request.json

def insert_https_parameters(sub_controller: SubController, parameters_names: List[str]):
    """Decorator with a purpose to insert parameters into a callable function in a https flask request"""
    def decorator(function):
        def callable():
            return function(self=sub_controller, **get_parameters(parameters_names))
        callable.__name__ = function.__name__
        return callable
    return decorator


class MainController(ABC):
    """Responsible for controlling the application"""

    @abstractmethod
    def run(self) -> None:
        """Runs the application."""
        pass

    @abstractmethod
    def add_resources(self, sub_controller: SubController) -> None:
        """Add resources from the other controllers"""
        pass


class FlaskController(MainController):
    """Responsible for controlling the application via Flask RESTful API."""

    def __init__(self, user_controller: UserController, debug: bool = True) -> None:
        """Initializes the API and its endpoints"""
        self.debug: bool = debug
        self.app: Flask = Flask(__name__)
        self._home()
        self.add_resources(sub_controller=user_controller)

    def run(self) -> None:
        """Runs the application."""
        self.app.run(debug=self.debug)

    def add_resources(self, sub_controller: SubController) -> None:
        """Add resources from the other controlers"""
        resources = sub_controller.resources()
        for resource in resources:
            self.app.route(f"/{resource.endpoint}", methods=["POST", "GET"])(
                insert_https_parameters(sub_controller, resource.parameters)(resource.callable)
            )

    def _home(self) -> None:
        """Defines an api endpoint to check if the server ir running fine and well."""
        app = self.app
        @app.route("/")
        def home() -> dict:
            return {
                "code": 1,
                "message": "all good here!!"
            }       

