from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Any, List
from inspect import signature, getmembers


@dataclass
class Resource:
    callable: Callable[... , dict]
    endpoint: str
    parameters: List[str]


def router(endpoint: str):
    """
    Decorator to add to each method of a SubController implementation.
    Allows creation of a resource from that method when it is called from the Main Contoller.
    """
    def decorator(function):
        return Resource(
            callable=function,
            endpoint=endpoint,
            parameters=[param 
                for param in list(signature(function).parameters)
                if param != "self"
            ]
        )
    return decorator


class SubController(ABC):
    """
    Abstract class for subcontrollers.
    This subcontrollers are responsible for creating api resources (a callable, endpoint pair)
    They will be called from the main controller to add those resources.
    Following this implementation, all of the resources must have methods starting with 'res_'.

    It is also the subcontrollers responsibility to implement the error coding to communicate 
    the failures brought up as exceptions to the client.
    """

    def resources(self) -> List[Resource]:
        """Returns the list of resources to be added """
        return [
            method
            for method_name, method in getmembers(self)
            if method_name.startswith("res_")
        ]