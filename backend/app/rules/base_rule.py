from abc import ABC, abstractmethod
from models.schemas import Finding
from preprocessing.preprocessor import PreprocessedRequirement
class BaseRule(ABC):

    @abstractmethod
    def apply(self, req: PreprocessedRequirement) -> list[Finding]:
        pass