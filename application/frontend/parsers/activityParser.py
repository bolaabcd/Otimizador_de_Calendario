
from typing import Optional
from ...domain.domainTypes import Activity
from .scheduleParser import parseSchedule


def parseActivity(data: dict) -> Optional[Activity]:
    try:
        schedules = []

        for scheduleDict in data['schedules']:
            schedule = parseSchedule(scheduleDict)
            if schedule is None:
                return None
            schedules.append(schedule)
        
        locations = data['locations']
        if len(schedules) != len(locations):
            return None
        
        for location in locations:
            if type(location) is not str:
                return None

        people = data['people']
        if len(schedules) != len(people):
            return None
        
        for person in people:
            if type(person) is not str:
                return None
        
        value = data['value']
        if type(value) is not float:
            return None

        return Activity(schedules, locations, people, value)
        
    except:
        return None