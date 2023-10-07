
from abc import ABC, abstractmethod
from .domainTypes import Activity, User
from typing import List, Tuple


class IGetCalendarService(ABC):

    @abstractmethod
    def getCalendar(self, user: User) -> List[dict]:
        pass
    
