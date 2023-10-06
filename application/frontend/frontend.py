
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from ..domain.domain import Domain
from ..domain.domainTypes import Activity, Schedule, Interval
from ..models import ActivityDB, ScheduleDB, PersonDB, LocationDB, IntervalDB
from ..solver.solver import ConcreteSolver
from django.http import JsonResponse
import json

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
        if request.method == 'POST':
            postData = request.body.decode('utf-8')
            try:
                json_data = json.loads(postData)
                acts = []
                for actDict in json_data:
                    actDB = ActivityDB(value = actDict['value'])
                    actDB.save()
                    for locStr in actDict['locations']:
                        locDB = LocationDB(name = locStr, activity = actDB)
                        locDB.save()
                    for persStr in actDict['people']:
                        persDB = PersonDB(name = persStr, activity = actDB)
                        persDB.save()
                    for schedList in actDict['schedules']:
                        schedDB = ScheduleDB(activity = actDB)
                        schedDB.save()
                        for intervList in schedList:
                            intervDB = IntervalDB(start_date = intervList[0], end_date = intervList[1], schedule = schedDB)
                            intervDB.save()

                return HttpResponse()
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'JSON PARSING ERROR'}, status=400)
        else:
            return HttpResponseNotAllowed(['POST'])

    def deleteCalendar(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'DELETE':
            ActivityDB.objects.all().delete()
            return HttpResponse()
        else:
            return HttpResponseNotAllowed(['DELETE'])


    def getCalendar(self, request: HttpRequest) -> HttpResponse:
        dbres = ActivityDB.objects.all()
        ans = []
        for v in dbres:
            ans.append(v.toDict())
        return JsonResponse({'acts':ans})

    def optimizeCalendar(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            postData = request.body.decode('utf-8')
            try:
                json_data = json.loads(postData)
                acts = []
                for actDict in json_data:
                    locs = list(actDict['locations'])
                    peopl = list(actDict['people'])
                    scheds = []
                    for sched in actDict['schedules']:
                        intervLists = []
                        for intervList in sched:
                            intervLists.append(Interval(intervList[0],intervList[1]))
                        schedConv = Schedule(intervLists)
                        scheds.append(schedConv)
                    actConv = Activity(schedules=scheds, locations=locs, people=peopl, value=actDict['value'])
                    acts.append(actConv)

                sol = ConcreteSolver()
                sol.solve(acts)

                return HttpResponse()
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'JSON PARSING ERROR'}, status=400)
        else:
            return HttpResponseNotAllowed(['POST'])
        pass
    
