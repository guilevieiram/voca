from flask import Flask, request, abort
from flask_cors import CORS
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from json import loads

from .sub_controller import Resource, SubController 
from .user_controller import UserController


def ger_request_parameters(parameters_names: List[str]) -> Dict[str, Any]:
    """Get parameters from the desired api call"""
    if not request.json or set(request.json.keys()) != set(parameters_names):
        abort(400)
    return request.json

def insert_https_parameters(sub_controller: SubController, parameters_names: List[str]):
    """Decorator with a purpose to insert parameters into a callable function in a https flask request"""
    def decorator(function):
        def callable():
            return function(self=sub_controller, **ger_request_parameters(parameters_names))
        callable.__name__ = function.__name__
        return callable
    return decorator


class MainController(ABC):
    """Responsible for controlling the application"""

    @abstractmethod
    def __init__(self, user_controller: UserController):
        """Initialises the controller with the necessary subcontrollers and adds the resources from those subcontrollers."""
        pass

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

    def __init__(self, user_controller: UserController) -> None:
        """Initializes the API and its endpoints"""
        self.app: Flask = Flask(__name__)
        self._home()
        self.add_resources(sub_controller=user_controller)

    def run(self, debug: bool = True) -> None:
        """Runs the application."""
        self.app.run(debug=debug)

    def add_resources(self, sub_controller: SubController) -> None:
        """Add resources from the other controlers"""
        resources = sub_controller.resources()
        for resource in resources:
            self.app.route(f"/{resource.endpoint}", methods=["POST", "GET"])(
                insert_https_parameters(sub_controller, resource.parameters)(resource.callable)
            )

    def _home(self) -> None:
        """Defines an api endpoint to check if the server ir running fine and well."""
        @self.app.route("/")
        def home() -> dict:
            return {
                "code": 1,
                "message": "all good here!!"
            }       


class TerminalController(MainController):
    """Responsible for controlling the application via terminal."""

    def __init__(self, user_controller: UserController) -> None:
        """Initializes the controller with its endpoints"""
        self.on: bool = True
        self.resources: Dict[str, Tuple[Resource, SubController]] = {}
        self.add_resources(sub_controller=user_controller)
        
    def run(self) -> None:
        """Runs the application."""
        while self.on:
            endpoint: str = input("\n~ ")
            if endpoint in ["exit", "EXIT", "Exit", "e", "exit()"]:
                self.on = False
            elif endpoint not in list(self.resources.keys()): 
               print("Command not valid.\n") 
            else:
                self._execute_task(endpoint=endpoint)
    
    def add_resources(self, sub_controller) -> None:
        """Add resources from the other controlers"""
        for resource in sub_controller.resources():
            self.resources[resource.endpoint] = (resource, sub_controller)

    def _execute_task(self, endpoint: str) -> dict:
        """Executes a given task given its endpoints"""
        resource, sub_controller = self.resources.get(endpoint)
        parameters: dict = loads(input("pars: "))
        if set(resource.parameters) == set(parameters.keys()):
            print(resource.callable(sub_controller, **parameters))
        else:
            print("\n Parameters not valid.")
