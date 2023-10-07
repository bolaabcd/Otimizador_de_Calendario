
from abc import ABC, abstractmethod
from .domainTypes import User


class IAuthUserService(ABC):

    @abstractmethod
    def authUser(self, user: User) -> bool:
        pass
    