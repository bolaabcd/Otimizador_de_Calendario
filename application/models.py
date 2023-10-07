from django.db import models
from .domain.domainTypes import Activity
import json

# Create your models here.

class UserDB(models.Model):
    name = models.CharField(max_length=100, unique = True)
    password = models.CharField(max_length=100)

class ActivityDB(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(UserDB, on_delete = models.CASCADE)
    
    def toDict(self):
        dic = {'value': self.value};
        people = self.persondb_set.all()
        dic['people'] = [str(p) for p in people]
        locations = self.locationdb_set.all()
        dic['locations'] = [str(l) for l in locations]
        schedules = self.scheduledb_set.all()
        dic['schedules'] = [s.toList() for s in schedules]
        return dic

class ScheduleDB(models.Model):
    activity = models.ForeignKey(ActivityDB, on_delete = models.CASCADE)
    def toList(self):
        intervals = self.intervaldb_set.all()
        return [i.toList() for i in intervals]

class IntervalDB(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    schedule = models.ForeignKey(ScheduleDB, on_delete = models.CASCADE)
    def toList(self):
        return [self.start_date, self.end_date]

class PersonDB(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(ActivityDB, on_delete = models.CASCADE)
    def __str__(self):
        return self.name

class LocationDB(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(ActivityDB, on_delete = models.CASCADE)
    def __str__(self):
        return self.name
