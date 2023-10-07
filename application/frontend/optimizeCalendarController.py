
from .IOptimizeCalendarController import IOptimizeCalendarController
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .requestsParser import RequestsParser
from .parsers.userParser import parseUser
from .parsers.calendarParser import parseCalendar
from ..domain.IOptimizeCalendarService import IOptimizeCalendarService
from typing import List

class OptimizeCalendarController(IOptimizeCalendarController):

    def __init__(self, requests: RequestsParser, service: IOptimizeCalendarService):
        self.__requests = requests
        self.__service = service

    def optimizeCalendar(self, request: HttpRequest) -> HttpResponse:
        data = self.__requests.getData(request)

        user = parseUser(data)
        if user is None:
            return HttpResponseBadRequest()
        
        calendar = parseCalendar(data)

        if calendar is None:
            return HttpResponseBadRequest()
        
        result = self.__service.optimizeCalendar(calendar)
        data = {'activities': result}
        return self.__requests.sendData(data)
    
