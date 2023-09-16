
from ..solver.solver import Solver

from ..storage.storage import Storage

from ..domain.domainTypes import User, Activity

from typing import Optional, Tuple, List


class Domain:

    def __init__(self):
        # self.solver = Solver()
        # self.storage = Storage()
        pass

    def createUser(self, user: User) -> bool:
        storedUser = self.__storage.findUser(user.name)
        if storedUser is None:
            self.__storage.createUser(user)
            return True
        else:
            return False

    def authUser(self, user: User) -> bool:
        storedUser = self.__storage.findUser(user.name)
        if storedUser is None:
            return False

        if storedUser.password == user.password:
            return True

        return False
    

    def loadCalendar(self, user: User) -> Optional[Tuple[
        List[Activity],
        List[Activity]
    ]]:
        if not self.authUser(user):
            return None
        
        return self.__storage.loadCalendar(user)

    def saveCalendar(
        self,
        user: User,
        queryActivities: List[Activity],
        optimizedActivities: List[Activity]
    ) -> bool:
        if not self.authUser(user):
            return False
        
        return self.__storage.saveCalendar(user, queryActivities, optimizedActivities)
    
    def optimizeCalendar(
        self,
        user: User,
        activities: List[Activity]
    ) -> Optional[List[Activity]]:
        if not self.authUser(user):
            return None
        
        return self.__solver.solve(activities)



    __solver: Solver
    __storage: Storage