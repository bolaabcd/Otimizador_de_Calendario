
from .IGetCalendarController import IGetCalendarController
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .requestsParser import RequestsParser
from .parsers.userParser import parseUser
from ..domain.IGetCalendarService import IGetCalendarService

class GetCalendarController(IGetCalendarController):

    def __init__(self, requests: RequestsParser, service: IGetCalendarService):
        self.__requests = requests
        self.__service = service

    def getCalendar(self, request: HttpRequest) -> HttpResponse:
        data = self.__requests.getData(request)
        if type(data) is not dict:
            return data

        user = parseUser(data)
        if user is None:
            return HttpResponseBadRequest()
        result = self.__service.getCalendar(user)
        data = {'activities': result}
        return self.__requests.sendData(data)
        
