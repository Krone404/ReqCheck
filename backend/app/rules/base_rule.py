from abc import ABC, abstractmethod
from app.models.schemas import Finding
from app.preprocessing.preprocessor import PreprocessedRequirement
class BaseRule(ABC):

    @abstractmethod
    def apply(self, req: PreprocessedRequirement) -> list[Finding]:
        pass