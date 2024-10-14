from AcademicCalendar.models.TimeStampedModel import TimeStampedModel
from AcademicCalendar.models.Organization import Organization

from django.db import models

class AcademicCalendar(TimeStampedModel):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True, max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.organization.name + ' - ' + self.description