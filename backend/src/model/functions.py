from abc import ABC, abstractmethod
import math

def instantiate(cls):
    class wrapper(cls):
        pass
    return wrapper()

class ConversionFunction(ABC):
    @staticmethod
    @abstractmethod
    def calculate(similarity_score: float) -> int:
        """Converts a float betweei 0 and 1 in a positive integer."""

@instantiate
class FloorConversion(ConversionFunction):
    @staticmethod
    def calculate(similarity_score: float) -> int:
        """Converts a float betweei 0 and 1 in a positive integer. Uses a scaled floor function."""
        return math.floor(similarity_score * 100)