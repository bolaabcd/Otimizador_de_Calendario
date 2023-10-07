
from django.http import HttpRequest, HttpResponse
from abc import ABC, abstractmethod
from typing import Union

class RequestsParser(ABC):

    @abstractmethod
    def getData(self, request: HttpRequest) -> Union[dict, HttpResponse]:
        pass

    @abstractmethod
    def sendData(self, data: dict) -> HttpRequest:
        pass

