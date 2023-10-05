
from abc import ABC, abstractmethod
from ..domain.domainTypes import Activity
from typing import List
from converter import ActivityIDs, getProblem, seeSolution #TODO: REMOVE THIS LAST ONE AFTER DEBUGGING
from pulp import GLPK


class Solver(ABC):

    @abstractmethod
    def solve(self, activities: List[Activity]) -> List[Activity]:
        pass



class concreteSolver(Solver):
    
    def solve(self, activities: List[Activity]) -> List[Activity]:
        # Converting to format that can be used by Integer Programming Solver:
        placesSet = set()
        peopleSet = set()
        timesSet = set()
        activityList = []
        for activ in activities:
            vals = []
            timList = []
            placList = []
            peopList = []
            for sched in activ.schedules:
                schedList = []
                for start, end in sched.intervs:
                    schedList += [start,end]
                timesSet.add(schedList)
                timList.append(schedList)
            for loc in activ.locations:
                placesSet.add(loc)
                peopList.append(loc)
            for peop in activ.people:
                peopleSet.add(peop)
                peopList.append(peop)
            activityList.append(vals)
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
            timesList.append(time)
        activitiesID = []
        for i,act in enumerate(activityList):
            timesID = []
            placesID = []
            peopleID = []
            for tims in act[0]:
                timesID.append(timesDict[tims])
            for placs in act[1]:
                placesID.append(placesDict[placs])
            for peop in act[2]:
                peopleID[peop]
            activID = ActivityIDs(timesID,placesID,peopleID,act[3])
            activitiesID.append(activID)
       prob = getProblem(timesList,len(placesList),len(peopleList),activitiesID)

        # TODO:REMOVE AFTER DEBUGGED:
        seeSolution(prob)

        # Converting solution to output format

        # recover original values from the IDs selected
