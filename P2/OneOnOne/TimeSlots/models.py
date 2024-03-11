from django.db import models
#from calendars.models import Calendar

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    owner = models.CharField(max_length=20)
    #calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)