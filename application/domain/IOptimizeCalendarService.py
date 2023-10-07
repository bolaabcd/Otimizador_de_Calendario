
from abc import ABC, abstractmethod
from .domainTypes import Activity, User
from typing import List, Optional

class IOptimizeCalendarService(ABC):

    @abstractmethod
    def optimizeCalendar(self, calendar: List[Activity], user: User) -> Optional[List[Activity]]:
        pass
    
