from abc import ABC, abstractmethod
from models.schemas import Finding

class BaseRule(ABC):

    @abstractmethod
    def apply(self, text: str) -> list[Finding]:
        pass