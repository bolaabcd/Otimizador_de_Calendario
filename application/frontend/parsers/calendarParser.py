
from typing import Optional, List
from ...domain.domainTypes import Activity
from .activityParser import parseActivity


def parseCalendar(data: List[dict]) -> Optional[List[Activity]]:
    try:
        activities = []
        for activityDict in data:
            activity = parseActivity(activityDict)
            if activity is None:
                return None
            activities.append(activity)
        
        return activities

    except:
        return None
