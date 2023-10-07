
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
        data = self.__requests.getData(request)
        if type(data) is not dict:
            return data

        user = parseUser(data)
        if user is None:
            return HttpResponseBadRequest()
        result = self.__service.deleteCalendar(user)
        data = {'delete': result}
        return self.__requests.sendData(data)

