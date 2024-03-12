from django.db import models
from Calendars.models import Day

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    owner = models.CharField(max_length=20)
    day = models.ForeignKey(Day, related_name="timeslots", on_delete=models.CASCADE)