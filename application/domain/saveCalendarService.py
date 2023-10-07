
from .ISaveCalendarService import ISaveCalendarService
from .IAuthUserService import IAuthUserService
from .domainTypes import Activity, User
from typing import List
from ..storage.storage import Storage


class SaveCalendarService(ISaveCalendarService):

    def __init__(self, storage: Storage, auth: IAuthUserService):
        self.__storage = storage
        self.__auth = auth

    def saveCalendar(self, calendar: List[Activity]) -> bool:

        result = self.__storage.saveCalendar(calendar)
        return result
    
