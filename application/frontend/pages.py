
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


class Pages:
    
    def getAuthPage(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'authpage.html')
    
    def getHomePage(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'homepage.html')
    