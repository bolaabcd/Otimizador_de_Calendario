
from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse


class IGetCalendarController(ABC):

    @abstractmethod
    def getCalendar(self, request: HttpRequest) -> HttpResponse:
        pass
    
