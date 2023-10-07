
from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse


class ICreateUserController(ABC):

    @abstractmethod
    def createUser(self, request: HttpRequest) -> HttpResponse:
        pass
    