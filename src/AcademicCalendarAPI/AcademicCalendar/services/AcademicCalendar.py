from AcademicCalendar.helpers.DaysCounterHelper import DaysCounterHelper
from AcademicCalendar.models import Semester
from AcademicCalendar.services.BaseService import BaseService
from AcademicCalendar.services.Semester import SemesterService

class AcademicCalendarService(BaseService):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.semesterService = SemesterService(*args, **kwargs)

    def schoolDaysSummary(self, calendar, campi):
        """
            Retorna a quantidade de dias letivos por semestre agrupado por campus
        """
        counting = {"total_days": 0, "sundays": 0}
        total_days = (calendar.end_date - calendar.start_date).days + 1

        sundays = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.SUNDAY_WEEK_DAY, calendar.start_date, calendar.end_date)
        saturdays = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.SATURDAY_WEEK_DAY, calendar.start_date, calendar.end_date)
        

        counting["total_days"] = total_days
        counting["saturdays"] = len(saturdays)
        counting["sundays"] = len(sundays)

        semesters_data = []
        
        semesters = self.getSemeters(calendar)

        for semester in semesters:
            semesters_data.append({ "description": semester.description, "campi_school_days_count":  self.semesterService.schoolDaysSummary(semester, campi)})
            
        counting["semesters"] = semesters_data

        return counting
    
    def getSemeters(self, calendar):
        return Semester.objects.filter(academic_calendar = calendar,organization__id = self.user.organization.id, deleted_at__isnull = True)