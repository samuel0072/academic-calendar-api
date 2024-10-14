from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException
import sys

from django.utils.translation import gettext as _

def validate_id(id) -> int:
    parsed_id = int(id)

    if(parsed_id > sys.maxsize):
        raise AcademicCalendarException(_("The passed id is not valid"))
    
    return parsed_id