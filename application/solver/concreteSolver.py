from .solver import Solver
from ..domain.domainTypes import Activity
from typing import List
from .converter import ActivityIDs, getProblem
from pulp import GLPK

class ConcreteSolver(Solver):
    
    def solve(self, activities: List[Activity]) -> List[Activity]:
        # Converting to a format that can be used by Integer Programming Solver:
        placesSet = set()
        peopleSet = set()
        timesSet = set()
        activityList = []
        for activ in activities:
            timList = []
            placList = []
            peopList = []
            for sched in activ.schedules:
                schedList = []
                for interv in sched.intervals:
                    start = interv.start
                    end = interv.end
                    schedList += [[start,end]]
                timesSet.add(str(schedList))
                timList.append(schedList)
            for loc in activ.locations:
                placesSet.add(loc)
                placList.append(loc)
            for peop in activ.people:
                peopleSet.add(peop)
                peopList.append(peop)
            actLi = []
            actLi.append(timList)
            actLi.append(placList)
            actLi.append(peopList)
            actLi.append(activ.value)
            activityList.append(actLi)
        placesDict = {}
        peopleDict = {}
        timesDict = {}
        placesList =  []
        peopleList = []
        timesList = []
        for i,place in enumerate(placesSet):
            placesDict[place] = i
            placesList.append(place)
        for i,person in enumerate(peopleSet):
            peopleDict[person] = i
            peopleList.append(person)
        for i,time in enumerate(timesSet):
            timesDict[time] = i
            timesList.append(eval(time))
        activitiesID = []
        for i,act in enumerate(activityList):
            timesID = []
            placesID = []
            peopleID = []
            for tims in act[0]:
                timesID.append(timesDict[str(tims)])
            for placs in act[1]:
                placesID.append(placesDict[placs])
            for peop in act[2]:
                peopleID.append(peopleDict[peop])
            activID = ActivityIDs(timesID,placesID,peopleID,act[3])
            activitiesID.append(activID)
        prob = getProblem(timesList,len(placesList),len(peopleList),activitiesID)

        prob.solve(GLPK())

        # Converting solution to output format
        actsAns = [{} for _ in activitiesID]
        for v in prob.variables():
            if v.name[0] == 'a': # activity
                actID = int(v.name[9:])
                actsAns[actID]['selected'] = v.varValue
            elif v.name[0] == 't': # time
                actID, timID = v.name[5:].split('_')
                actID = int(actID)
                timID = int(timID)
                actsAns[actID]['timID'] = int(timID)
            elif v.name[1] == 'e': # person
                actID, persID = v.name[7:].split('_')
                actID = int(actID)
                persID = int(persID)
                actsAns[actID]['persID'] = int(persID)
            elif v.name[1] == 'l': # place
                actID, placID = v.name[6:].split('_')
                actID = int(actID)
                placID = int(placID)
                actsAns[actID]['placID'] = int(placID)
            else:
                raise NotImplementedError()

        # recover original values from the IDs selected
        answer = []
        for i, actAns in enumerate(actsAns):
            act = {}
            if actAns['selected'] == 1:
                tims = timesList[actAns['timID']]
                act['schedules'] = [{'intervals':[{'start': t[0].replace('Z',''), 'end': t[1].replace('Z','')} for t in tims]}]
                act['locations'] = [placesList[actAns['placID']]]
                act['people'] = [peopleList[actAns['persID']]]
                act['value'] = activityList[i][3]
                answer.append(act)

        return answer
