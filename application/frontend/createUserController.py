
from .ICreateUserController import ICreateUserController
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .requestsParser import RequestsParser
from ..domain.ICreateUserService import ICreateUserService
from .parsers.userParser import parseUser

class CreateUserController(ICreateUserController):

    def __init__(self, requests: RequestsParser, service: ICreateUserService):
        self.__requests = requests
        self.__service = service
        
    def createUser(self, request: HttpRequest) -> HttpResponse:
        data = self.__requests.getData(request)
        if not (type(data) is dict):
            return data
        
        user = parseUser(data)
        if user is None:
            return HttpResponseBadRequest()

        result = self.__service.createUser(user)
        data = {'create': result}
        return self.__requests.sendData(data)

