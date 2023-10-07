
from abc import ABC, abstractmethod
from ..domain.domainTypes import User, Activity
from typing import Optional, Tuple, List


class Storage(ABC):

    @abstractmethod
    def createUser(self, user: User) -> bool:
        pass

    @abstractmethod
    def findUser(self, name: str) -> Optional[User]:
        pass

    @abstractmethod
    def loadCalendar(self, user: User) -> Optional[List[Activity]]:
        pass

    @abstractmethod
    def saveCalendar(
        self,
        activities: List[Activity],
        user: User
    ) -> bool:
        pass

    @abstractmethod
    def deleteCalendar(self, user: User) -> bool:
        pass
