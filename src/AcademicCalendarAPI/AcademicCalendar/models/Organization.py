from AcademicCalendar.models import TimeStampedModel
from django.db import models

class Organization(TimeStampedModel):
    name = models.TextField(max_length=150)
    minutes_per_lesson = models.IntegerField()
    min_minutes_per_day = models.IntegerField()

    def __str__(self) -> str:
        return self.name