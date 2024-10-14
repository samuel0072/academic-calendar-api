from AcademicCalendar.services.BaseService import BaseService
from AcademicCalendar.services.Campus import CampusService

class SemesterService(BaseService):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.campusService = CampusService(*args, **kwargs)

    def schoolDaysSummary(self, semester, campi):
        """
            Retorna um set com todas as datas que são dias letivos no semestre.
        """
        campi_school_days = []

        for campus in campi:
            campus_summary = self.campusService.schoolDaysSummaryForAcademicCalendar(semester.academic_calendar, campus, semester.lessons_start_date, semester.lessons_end_date)

            campi_school_days.append({ "id": campus.id, "name": campus.name, "school_days_count": len(campus_summary)})
        
        return campi_school_days