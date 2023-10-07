from abc import ABC, abstractmethod
from django.http import HttpRequest, HttpResponse


class IAuthUserController(ABC):

    @abstractmethod
    def authUser(self, request: HttpRequest) -> HttpResponse:
        pass
    
