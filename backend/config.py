"""
This is the configuration file for the backend application.
All the raw configurations are setted in the 'configurations.json' file in the root directory.
This class is to be utilized only by the app.py file.
"""

from typing import List, Dict
from json import load
import os


def instantiate(cls):
    class wrapper(cls):
        pass
    return wrapper()


@instantiate
class Configurations:
    """Configuration class, not to be instantiated but to be utilized to get the configurations from the raw config file."""

    configuration_file: str = "configurations.json"

    @property
    def database_url(self) -> str:
        """Returns the database url."""
        with open(self.configuration_file, encoding="utf-8") as file:
            database_url_env_name: str = load(file).get("postgresqlDatabase")
        return os.environ.get(database_url_env_name)

    @property
    def debug(self) -> bool:
        """Returns a boolean to say if the debug mode is active."""
        with open(self.configuration_file, encoding="utf-8") as file:
            return load(file).get("debug")

    @property
    def supported_languages(self) -> List[Dict[str, str]]:
        """Return all the supported languages of the backend application."""
        with open(self.configuration_file, encoding="utf-8") as file:
            return load(file).get("supportedLanguages")
        
    @property
    def supported_languages_codes(self) -> List[str]:
        """Return the list with all the codes for the supported languages."""
        return [language.get("code") for language in self.supported_languages]