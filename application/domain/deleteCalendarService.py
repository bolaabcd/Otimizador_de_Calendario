
from .IDeleteCalendarService import IDeleteCalendarService
from .IAuthUserService import IAuthUserService
from .domainTypes import User
from ..storage.storage import Storage

class DeleteCalendarService(IDeleteCalendarService):

    def __init__(self, storage: Storage, auth: IAuthUserService):
        self.__storage = storage
        self.__auth = auth

    def deleteCalendar(self) -> bool:
        
        return self.__storage.deleteCalendar()
    
    
