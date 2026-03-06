from abc import ABC, abstractmethod
from preprocessing.preprocessor import PreprocessedRequirement
from models.schemas import Finding
class BaseRule(ABC):

    @abstractmethod
    def apply(self, req: PreprocessedRequirement) -> list[Finding]:
        pass