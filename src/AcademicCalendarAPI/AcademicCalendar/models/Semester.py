from AcademicCalendar.models import TimeStampedModel
from AcademicCalendar.models.Organization import Organization
from AcademicCalendar.models import AcademicCalendar
from AcademicCalendar.models.Campus import Campus

from AcademicCalendar.helpers.CampusSchoolDaysSummary import CampusSchoolDaysSummary

from django.db import models
from django.db.models import QuerySet

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
    
    def schoolDaysSummary(self, campi: QuerySet[Campus]):
        """
            Retorna um set com todas as datas que são dias letivos no semestre.
        """
        campi_school_days = []

        for campus in campi:
            campus_summary = CampusSchoolDaysSummary.schoolDaysSummaryForAcademicCalendar(self.academic_calendar, campus, self.lessons_start_date, self.lessons_end_date)

            campi_school_days.append({ "id": campus.id, "name": campus.name, "school_days_count": len(campus_summary)})
        
        return campi_school_days