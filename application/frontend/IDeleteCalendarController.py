
from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse


class IDeleteCalendarController(ABC):

    @abstractmethod
    def deleteCalendar(self, request: HttpRequest) -> HttpResponse:
        pass
    
