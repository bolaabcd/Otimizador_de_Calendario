from django.db import models
from .domain.domainTypes import Activity

# Create your models here.

class ActivityDB(models.Model):
    value = models.IntegerField()

    def get_activity(self):
    # TODO: Retornar mais que soh o valor
        return self.value

class ScheduleDB(models.Model):
    activity = models.ForeignKey(ActivityDB, on_delete = models.CASCADE)

class IntervalDB(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.ForeignKey(ScheduleDB, on_delete = models.CASCADE)

class PersonDB(models.Model):
    name = models.CharField(max_length=100)
    activity = models.ForeignKey(ActivityDB, on_delete = models.CASCADE)

class LocationDB(models.Model):
    loc = models.CharField(max_length=100)
    activity = models.ForeignKey(ActivityDB, on_delete = models.CASCADE)



    
