
from abc import ABC, abstractmethod
from .domainTypes import User


class IDeleteCalendarService(ABC):

    @abstractmethod
    def deleteCalendar(self, user: User) -> bool:
        pass
    
