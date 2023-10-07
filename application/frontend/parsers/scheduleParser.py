
from typing import Optional
from ...domain.domainTypes import Schedule
from .intervalParser import parseInterval


def parseSchedule(data: dict) -> Optional[Schedule]:
    try:
        intervals = []

        for intervalPair in data:
            interval = parseInterval(intervalPair)
            if interval is None:
                return None
            intervals.append(interval)
        
        return Schedule(intervals)

    except:
        return None
    
