from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from abc import ABC, abstractmethod


class Controller(ABC):
    """Responsible for controlling the application"""

    @abstractmethod
    def run(self) -> None:
        """Runs the application."""
        pass

class FlaskController(Controller):
    """Responsible for controlling the application via Flask RESTful API."""

    def __init__(self, debug: bool = True) -> None:
        """Initializes the API and its endpoints"""
        self.debug: bool = debug
        self.app: Flask = Flask(__name__)
        self.cors = CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.api: Api = Api(self.app)

        self.api.add_resource(self._home(), '/')

    def run(self) -> None:
        """Runs the application."""
        self.app.run(debug=self.debug)


    def _home(self) -> Resource:
        """Defines an api endpoint to check if the server ir running fine and well."""
        class _home(Resource):
            def get(self):
                return {
                    "code": 1,
                    "message": "all good here!!"
                }       
        return _home   

