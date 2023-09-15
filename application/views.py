
from application.frontend.frontend import Frontend
from django.http import HttpRequest, HttpResponse


def homepage(request: HttpRequest) -> HttpResponse:
    return Frontend().getHomePage(request)

def authPage(request: HttpRequest) -> HttpResponse:
    return Frontend().getAuthPage(request)

def createUser(request: HttpRequest) -> HttpResponse:
    return Frontend().createUser(request)

def authUser(request: HttpRequest) -> HttpResponse:
    return Frontend().authUserUser(request)

def saveCalendar(request: HttpRequest) -> HttpResponse:
    return Frontend().saveCalendar(request)

def getCalendar(request: HttpRequest) -> HttpResponse:
    return Frontend().getCalendar(request)

def optimizeCalendar(request: HttpRequest) -> HttpResponse:
    return Frontend().optimizeCalendar(request)

