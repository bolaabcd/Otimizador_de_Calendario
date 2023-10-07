
from abc import ABC, abstractmethod
from .domainTypes import Activity, User
from typing import List

class ISaveCalendarService(ABC):

    @abstractmethod
    def saveCalendar(self, calendar: List[Activity]) -> bool:
        pass
    
