from .storage import Storage
from ..domain.domainTypes import User, Activity
from typing import Optional, List
from ..models import UserDB, ActivityDB, ScheduleDB, IntervalDB, PersonDB, LocationDB

class ConcreteStorage(Storage):

    def createUser(self, user: User) -> bool:
        # Create a new user in the database with the provided User object
        userDB = UserDB(name=user.name, password=user.password)
        userDB.save()
        return True

    def findUser(self, name: str) -> Optional[User]:
        # Find and return a user from the database based on their name
        user = UserDB.objects.filter(name=name)
        if len(user) != 1:
            return None
        else:
            return user[0]

    def loadCalendar(self, user: User) -> Optional[List[dict]]:
        # Load the user's calendar from the database and return it as a list of dictionaries
        usDB = self.findUser(user.name)
        dbres = ActivityDB.objects.filter(user=usDB)
        ans = []
        for v in dbres:
            ans.append(v.toDict())
        return ans

    def saveCalendar(
        self,
        activities: List[Activity],
        user: User
    ) -> bool:
        # Save a list of activities to the user's calendar in the database
        self.deleteCalendar(user)
        usDB = self.findUser(user.name)
        acts = []
        for activ in activities:
            actDB = ActivityDB(value=activ.value, user=usDB)
            actDB.save()
            for locStr in activ.locations:
                locDB = LocationDB(name=locStr, activity=actDB)
                locDB.save()
            for persStr in activ.people:
                persDB = PersonDB(name=persStr, activity=actDB)
                persDB.save()
            for sched in activ.schedules:
                schedList = sched.intervals
                schedDB = ScheduleDB(activity=actDB)
                schedDB.save()
                for interv in schedList:
                    intervList = [interv.start, interv.end]
                    intervDB = IntervalDB(start_date=intervList[0], end_date=intervList[1], schedule=schedDB)
                    intervDB.save()
        return True

    def deleteCalendar(self, user: User) -> bool:
        # Delete all activities from the user's calendar in the database
        usDB = self.findUser(user.name)
        ActivityDB.objects.filter(user=usDB).delete()
        return True
