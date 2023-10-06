
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from ..domain.domain import Domain
from ..models import ActivityDB#, ScheduleDB, PersonDB, LocationDB, IntervalDB
from django.http import JsonResponse

class Frontend:

    def __init__(self) -> None:
        self.__domain = Domain() 


    def getAuthPage(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass

    def getHomePage(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'homepage.html')

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
        dbres = ActivityDB.objects.all()
        ans = []
        for v in dbres:
            ans.append(v.toDict())
        return JsonResponse({'acts':ans})

    def optimizeCalendar(self, request: HttpRequest) -> HttpResponse:
        # TODO
        pass
    
