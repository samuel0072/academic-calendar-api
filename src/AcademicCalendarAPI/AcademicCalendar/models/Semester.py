from AcademicCalendar.models import TimeStampedModel
from AcademicCalendar.models.Organization import Organization
from AcademicCalendar.models import AcademicCalendar

from django.db import models

class Semester(TimeStampedModel):
    start_date = models.DateField()
    end_date = models.DateField()
    lessons_start_date = models.DateField()
    lessons_end_date = models.DateField()
    description = models.TextField(max_length=150)
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.description + ' - ' + self.academic_calendar.__str__()