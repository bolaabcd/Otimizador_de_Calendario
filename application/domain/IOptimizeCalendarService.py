
from abc import ABC, abstractmethod
from .domainTypes import Activity, User
from typing import List, Optional

class IOptimizeCalendarService(ABC):

    @abstractmethod
    def optimizeCalendar(self, user: User, calendar: List[Activity]) -> Optional[List[Activity]]:
        pass
    
