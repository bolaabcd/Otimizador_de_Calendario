
from .IDeleteCalendarService import IDeleteCalendarService
from .IAuthUserService import IAuthUserService
from .domainTypes import User
from ..storage.storage import Storage

class DeleteCalendarService(IDeleteCalendarService):

    def __init__(self, storage: Storage, auth: IAuthUserService):
        self.__storage = storage
        self.__auth = auth

    def deleteCalendar(self, user: User) -> bool:
        if not self.__auth.authUser(user):
            return False
        
        return self.__storage.deleteCalendar(user)
    
    