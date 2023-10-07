
from abc import ABC, abstractmethod
from .domainTypes import Activity, User
from typing import List

class ISaveCalendarService(ABC):

    @abstractmethod
    def saveCalendar(self, user: User, unoptimizedCalendar: List[Activity], optimizedCalendar: List[Activity]) -> bool:
        pass
    
