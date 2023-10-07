
from ..frontend.requestsParser import RequestsParser

from django.http import JsonResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse
from typing import Union
import json


class JSONRequest(RequestsParser):
    
    def getData(self, request: HttpRequest) -> Union[dict, HttpResponse]:
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        
        try:
            return json.loads(request.body.decode('utf-8'))
        except:
            return HttpResponseBadRequest()
    
    def sendData(self, data: dict) -> HttpRequest:
        return JsonResponse(data)
    
