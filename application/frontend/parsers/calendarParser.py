
from typing import Optional, List
from ...domain.domainTypes import Activity
from .activityParser import parseActivity


def parseCalendar(data: dict) -> Optional[List[Activity]]:
    try:
        activities = []

        for activityDict in data['activities']:
            activity = parseActivity(activityDict)
            if activity is None:
                return None
            activities.append(activities)
        
        return activities

    except:
        return None
