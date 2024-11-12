from AcademicCalendar.models.TimeStampedModel import TimeStampedModel
from AcademicCalendar.models.Organization import Organization
from django.db import models

class Campus(TimeStampedModel):
    name = models.TextField(max_length=150)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name