
from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse


class ISaveCalendarController(ABC):

    @abstractmethod
    def saveCalendar(self, request: HttpRequest) -> HttpResponse:
        pass
    
