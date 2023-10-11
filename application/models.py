from django.db import models

# User model to store user information
class UserDB(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    password = models.CharField(max_length=1000)

# Activity model to represent user activities
class ActivityDB(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(UserDB, on_delete=models.CASCADE)

    def toDict(self):
        # Convert the activity to a dictionary for serialization
        dic = {'value': self.value}
        people = self.persondb_set.all()
        dic['people'] = [str(p) for p in people]
        locations = self.locationdb_set.all()
        dic['locations'] = [str(l) for l in locations]
        schedules = self.scheduledb_set.all()
        dic['schedules'] = [s.toDict() for s in schedules]
        return dic

# Schedule model to represent schedules associated with activities
class ScheduleDB(models.Model):
    activity = models.ForeignKey(ActivityDB, on_delete=models.CASCADE)

    def toDict(self):
        intervals = self.intervaldb_set.all()
        return {'intervals': [i.toDict() for i in intervals]}

# Interval model to represent time intervals in a schedule
class IntervalDB(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    schedule = models.ForeignKey(ScheduleDB, on_delete=models.CASCADE)

    def toDict(self):
        return {'start': self.start_date, 'end': self.end_date}

# Person model to store information about people associated with activities
class PersonDB(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(ActivityDB, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Location model to store information about locations associated with activities
class LocationDB(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(ActivityDB, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  # String representation of the location
