
from .IGetCalendarService import IGetCalendarService
from .IAuthUserService import IAuthUserService
from .domainTypes import User, Activity
from ..storage.storage import Storage
from typing import List, Tuple

class GetCalendarService(IGetCalendarService):

    def __init__(self, storage: Storage, auth: IAuthUserService):
        self.__storage = storage
        self.__auth = auth

    def getCalendar(self, user: User) -> List[dict]:
        result = self.__storage.loadCalendar(user)
        if result is None:
            return []
        
        return result    
    
