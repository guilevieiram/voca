from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional, List

from .sub_controller import Resource, SubController, router

from src.model.user_model import User


class UserController(SubController):
    """
    UserController abstract class responsible for defining user related resources.
    All resources must have 
    """
        
    @router(endpoint="")
    @abstractmethod
    def res_login(self, user_email: str, password: str) -> dict:
        """Logs a user in and returns the dict message with the user id (if successfull)"""
        pass

    @router(endpoint="")
    @abstractmethod
    def res_sign_up(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> dict: 
        """Add a user in the system."""
        pass
        
    @router(endpoint="")
    @abstractmethod
    def res_delete_user(self, user_id: id) -> dict: 
        """Delete a user in the system."""
        pass
        
    @router(endpoint="")
    @abstractmethod
    def res_find_user(self, property: str, value: Any) -> dict: 
        """Find a user in the system."""
        pass
        
    @router(endpoint="")
    @abstractmethod
    def res_update_user(self, user_id: int, property: str, value: Any) -> dict: 
        """Update a user in the system."""
        pass


class DummyUserController(UserController):
    """
    UserController abstract class responsible for defining user related resources.
    All resources must have 
    """
    
    @router(endpoint="user/login")
    def res_login(self, user_email: str, password: str) -> dict:
        """Logs a user in and returns the dict message with the user id (if successfull)"""
        return {
            "code": 1,
            "message": f"User {user_email=} logged in.",
            "user_id": 0
        }
        pass

    @router(endpoint="user/add")
    def res_add_user(self, user_name: str, user_email: str, user_password: str, user_language: str, user_photo: Optional[str] = "") -> dict: 
        """Add a user in the system."""
        return {
            "code": 1,
            "message": f"Adding user with {user_name=}, {user_email=}, {user_password=}, {user_language=}, {user_photo=}"
        }

    @router(endpoint="user/delete")
    def res_delete_user(self, user_id: id) -> dict: 
        """Delete a user in the system."""
        return {
            "code": 1,
            "message": f"Deleting user with {user_id=}"
        }

    @router(endpoint="user/find")
    def res_find_user(self, property: str, value: Any) -> dict: 
        """Find a user in the system."""
        return {
            "code": 1,
            "message": f"Finding user with {property=}, {value=}"
        }

    @router(endpoint="user/update")
    def res_update_user(self, user_id: int, property: str, value: Any) -> dict: 
        """Update a user in the system."""
        return {
            "code": 1,
            "message": f"Updating user with {user_id=}, {property=}, {value=}"
        }