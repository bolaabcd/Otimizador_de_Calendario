
from .IOptimizeCalendarService import IOptimizeCalendarService
from .IAuthUserService import IAuthUserService
from ..solver.solver import Solver
from .domainTypes import Activity, User
from typing import List, Optional


class OptimizeCalendarService(IOptimizeCalendarService):

    def __init__(self, auth: IAuthUserService, solver: Solver):
        self.__auth = auth
        self.__solver = solver
        
    def optimizeCalendar(self, user: User, calendar: List[Activity]) -> Optional[List[Activity]]:
        if not self.__auth.authUser(user):
            return None
        
        optimized = self.__solver.solve(calendar)
        return optimized
    
    
