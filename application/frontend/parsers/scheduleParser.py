
from typing import Optional
from ...domain.domainTypes import Schedule
from .intervalParser import parseInterval


def parseSchedule(data: dict) -> Optional[Schedule]:
    try:
        scheduleDict = data['intervals']
        intervals = []

        for intervalDict in scheduleDict:
            interval = parseInterval(intervalDict)
            if interval is None:
                return None
            intervals.append(interval)
        
        return Schedule(intervals)

    except:
        return None
    