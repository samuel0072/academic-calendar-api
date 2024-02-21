from .base_importer import BaseEventImporter
from AcademicCalendar.models import Event, Organization
from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException

from django.core.files import File
from django.utils.translation import gettext as _

from pandas import read_excel

class NationalHolidayImporter(BaseEventImporter):
    DATE_COLUMN = 'data'
    NAME_COLUMN = 'nome'
    def __init__(self, file: File, organization: Organization) -> None:
        self.df = read_excel(file, parse_dates=True, header=0)
        columns = self.df.columns
        
        if not(self.DATE_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the date column'))
        
        if not(self.NAME_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the name column'))
        
        self.organization = organization
        super().__init__()

    def import_event(self) -> None:
        events = []
        for _, row in self.df.iterrows():
            
            event = Event(start_date=row[self.DATE_COLUMN], description=row[self.NAME_COLUMN])
            event.label = Event.HOLIDAY
            event.organization = self.organization
            events.append(event)

        Event.objects.bulk_create(events)