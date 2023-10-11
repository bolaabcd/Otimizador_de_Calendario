from .IAuthUserService import IAuthUserService
from .domainTypes import User
from ..storage.storage import Storage

class AuthUserService(IAuthUserService):

    # Constructor for the AuthUserService class
    def __init__(self, storage: Storage):
        self.__storage = storage

    def authUser(self, user: User) -> bool:
        storedUser = self.__storage.findUser(user.name)
        if storedUser is None:
            return False
        if storedUser.password != user.password:
            return False
        
        return True
