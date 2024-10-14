from AcademicCalendar.models import TimeStampedModel
from django.db import models

class Organization(TimeStampedModel):
    name = models.TextField(max_length=150)

    def __str__(self) -> str:
        return self.name