
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
        originalFormat = '%Y-%m-%dT%H:%M:%SZ'
        warnings.filterwarnings("ignore", category=RuntimeWarning) 
        return Interval(
            datetime.strptime(data['start'], originalFormat).strftime(dateFormat),
            datetime.strptime(data['end'], originalFormat).strftime(dateFormat)
        )
    except:
        return None
    
