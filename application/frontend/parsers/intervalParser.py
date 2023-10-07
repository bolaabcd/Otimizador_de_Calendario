
from typing import Optional
from ...domain.domainTypes import Interval
from datetime import datetime

def parseInterval(data: dict) -> Optional[Interval]:
    try:
        if not (type(data['start']) is str):
            return None
        if not (type(data['end']) is str):
            return None
        
        dateFormat = '%Y-%m-%d %H:%M:%S'

        return Interval(
            datetime.strptime(data['start'], dateFormat),
            datetime.strptime(data['end'],   dateFormat)
        )
    except:
        return None
    