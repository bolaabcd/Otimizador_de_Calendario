
from typing import Optional
from ...domain.domainTypes import Interval
from datetime import datetime
import warnings

def parseInterval(data: dict) -> Optional[Interval]:
    try:
        if not (type(data['start']) is str):
            return None
        if not (type(data['end']) is str):
            return None
        
        dateFormat = '%Y-%m-%d %H:%M:%S'
        originalFormat = '%Y-%m-%dT%H:%M:%S'
        warnings.filterwarnings("ignore", category=RuntimeWarning) 
        stdate = data['start'].replace('T', ' ')
        endate = data['end'].replace('T', ' ')
        if stdate[-1] != 'Z':
            stdate += 'Z'
        if endate[-1] != 'Z':
            endate += 'Z';
        return Interval(stdate, endate)
    except:
        return None
    
