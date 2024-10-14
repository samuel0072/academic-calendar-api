from AcademicCalendar.models.TimeStampedModel import TimeStampedModel
from AcademicCalendar.models.Organization import Organization
from AcademicCalendar.models.Campus import Campus

from AcademicCalendar.helpers.DaysCounterHelper import DaysCounterHelper

from django.db import models
from django.db.models import QuerySet

class AcademicCalendar(TimeStampedModel):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True, max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.organization.name + ' - ' + self.description
    
    def schoolDaysSummary(self, campi: QuerySet[Campus]):
        """
            Retorna a quantidade de dias letivos por semestre agrupado por campus
        """
        counting = {"total_days": 0, "sundays": 0}
        total_days = (self.end_date - self.start_date).days + 1

        sundays = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.SUNDAY_WEEK_DAY, self.start_date, self.end_date)
        saturdays = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.SATURDAY_WEEK_DAY, self.start_date, self.end_date)
        

        counting["total_days"] = total_days
        counting["saturday"] = len(saturdays)
        counting["sundays"] = len(sundays)

        semesters_data = []

        for semester in self.semesters:
            semesters_data.append({ "description": semester.description, "campi_school_days_count":  semester.schoolDaysSummary(campi)})
            
        counting["semesters"] = semesters_data

        return counting
    
    @property
    def semesters(self):
        return self._semesters
    
    @semesters.getter
    def semesters(self):
        return self._semesters
    
    @semesters.setter
    def semesters(self, semesters):
        self._semesters = semesters