
from abc import ABC, abstractmethod
from ..domain.domainTypes import Activity
from typing import List



class Solver(ABC):

    @abstractmethod
    def solve(self, activities: List[Activity]) -> List[Activity]:
        pass

