
from abc import ABC, abstractmethod
from .domainTypes import User


class ICreateUserService(ABC):

    @abstractmethod
    def authUser(self, user: User) -> bool:
        pass
    