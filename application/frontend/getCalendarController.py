
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
        if request.method == 'GET':
            result = self.__service.getCalendar()
            data = {'acts':result}
            return self.__requests.sendData(data)
        else:
            return HttpResponseNotAllowed(['GET'])
