
from .storage import Storage
from ..domain.domainTypes import User, Activity
from typing import Optional, Tuple, List
from ..models import UserDB, ActivityDB, ScheduleDB, IntervalDB, PersonDB, LocationDB


class ConcreteStorage(Storage):

    def createUser(self, user: User) -> bool:
        user = UserDB(name=user.name, password = user.password)
        user.save()
        return True

    def findUser(self, name: str) -> Optional[User]:
        user = UserDB.objects.filter(name=name)
        if len(user) != 1:
            return None
        else:
            return user[0]

    def loadCalendar(self) -> Optional[List[dict]]:
        dbres = ActivityDB.objects.all()
        ans = []
        for v in dbres:
            ans.append(v.toDict())
        return ans

    def saveCalendar(
        self,
        activities: List[Activity],
    ) -> bool:
        acts = []
        for activ in activities:
            actDB = ActivityDB(value = activ.value)
            actDB.save()
            for locStr in activ.locations:
                locDB = LocationDB(name = locStr, activity = actDB)
                locDB.save()
            for persStr in activ.people:
                persDB = PersonDB(name = persStr, activity = actDB)
                persDB.save()
            for sched in activ.schedules:
                schedList = sched.intervals
                schedDB = ScheduleDB(activity = actDB)
                schedDB.save()
                for interv in schedList:
                    intervList = [interv.start,interv.end]
                    intervDB = IntervalDB(start_date = intervList[0], end_date = intervList[1], schedule = schedDB)
                    intervDB.save()
        return True

    def deleteCalendar(self) -> bool:
        ActivityDB.objects.all().delete()
        return True
