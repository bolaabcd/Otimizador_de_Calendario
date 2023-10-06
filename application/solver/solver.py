
from abc import ABC, abstractmethod
from ..domain.domainTypes import Activity
from typing import List
from .converter import ActivityIDs, getProblem, seeSolution #TODO: REMOVE THIS LAST ONE AFTER DEBUGGING
from pulp import GLPK


class Solver(ABC):

    @abstractmethod
    def solve(self, activities: List[Activity]) -> List[Activity]:
        pass



class ConcreteSolver(Solver):
    
    def solve(self, activities: List[Activity]) -> List[Activity]:
        # Converting to format that can be used by Integer Programming Solver:
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
            print(i,act)
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

        # TODO:REMOVE AFTER DEBUGGED:
        seeSolution(prob)

        # Converting solution to output format

        # recover original values from the IDs selected
