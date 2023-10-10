
from .ISaveCalendarController import ISaveCalendarController
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .requestsParser import RequestsParser
from .parsers.userParser import parseUser
from .parsers.calendarParser import parseCalendar
from ..domain.ISaveCalendarService import ISaveCalendarService
from typing import List

class SaveCalendarController(ISaveCalendarController):

    def __init__(self, requests: RequestsParser, service: ISaveCalendarService):
        self.__requests = requests
        self.__service = service

    def saveCalendar(self, request: HttpRequest) -> HttpResponse:
        data = self.__requests.getData(request)

        user = parseUser(data)
        if user is None:
            return HttpResponseBadRequest()
        
        calendar = parseCalendar(data)
        if calendar is None:
            return HttpResponseBadRequest()
        result = self.__service.saveCalendar(calendar, user)
        data = {'save': result}
        return self.__requests.sendData(data)
    
