
from .IDeleteCalendarController import IDeleteCalendarController
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .requestsParser import RequestsParser
from .parsers.userParser import parseUser
from ..domain.IDeleteCalendarService import IDeleteCalendarService

class DeleteCalendarController(IDeleteCalendarController):

    def __init__(self, requests: RequestsParser, service: IDeleteCalendarService):
        self.__requests = requests
        self.__service = service

    def deleteCalendar(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'DELETE':
            result = self.__service.deleteCalendar()
            data = {'delete': result}
            return self.__requests.sendData(data)
        else:
            return HttpResponseNotAllowed(['DELETE'])
        
    
