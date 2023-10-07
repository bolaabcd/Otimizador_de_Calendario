
from .IAuthUserController import IAuthUserController
from ..domain.IAuthUserService import IAuthUserService
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .requestsParser import RequestsParser
from .parsers.userParser import parseUser

class AuthUserController(IAuthUserController):

    def __init__(self, requests: RequestsParser, service: IAuthUserService):
        self.__requests = requests
        self.__service = service

    def authUser(self, request: HttpRequest) -> HttpResponse:
        data = self.__requests.getData(request)
        if not (type(data) is dict):
            return data
        
        user = parseUser(data)
        if user is None:
            return HttpResponseBadRequest()

        result = self.__service.authUser(user)
        data = {'auth': result}
        return self.__requests.sendData(data)


        
