
from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse


class IOptimizeCalendarController(ABC):

    @abstractmethod
    def optimizeCalendar(self, request: HttpRequest) -> HttpResponse:
        pass
    
