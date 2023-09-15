
from django.http import HttpRequest, HttpResponse
from ..domain.domain import Domain

class Frontend:

    def __init__(self) -> None:
        self.__domain = Domain() 


    def getAuthPage(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass

    def getHomePage(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass

    def createUser(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass

    def authUser(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass

    def saveCalendar(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass

    def getCalendar(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass

    def optimizeCalendar(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass
    