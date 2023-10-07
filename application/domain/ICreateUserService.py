
from abc import ABC, abstractmethod
from .domainTypes import User


class ICreateUserService(ABC):

    @abstractmethod
    def createUser(self, user: User) -> bool:
        pass
    
