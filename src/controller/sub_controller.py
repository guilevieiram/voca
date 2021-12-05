from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Any, List
from inspect import signature


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
                if param is not "self"
            ]
        )
    return decorator


@dataclass
class Resource:
    callable: Callable[... , dict]
    endpoint: str
    parameters: List[str]


class SubController(ABC):
    """
    Abstract class for subcontrollers.
    This subcontrollers are responsible for creating api resources (a callable, endpoint pair)
    They will be called from the main controller to add those resources.
    """

    @abstractmethod
    def resources() -> List[Resource]:
        """Returns the list of resources to be added """
        pass