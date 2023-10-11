from .ICreateUserService import ICreateUserService
from .domainTypes import User
from ..storage.storage import Storage

class CreateUserService(ICreateUserService):

    # Constructor for the CreateUserService class
    def __init__(self, storage: Storage):
        self.__storage = storage

    def createUser(self, user: User) -> bool:
        storedUser = self.__storage.findUser(user.name)
        if storedUser is None:
            self.__storage.createUser(user)
            return True
        else:
            return False
