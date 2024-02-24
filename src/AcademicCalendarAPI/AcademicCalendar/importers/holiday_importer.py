from .base_importer import BaseEventImporter
from AcademicCalendar.models import Event, Organization
from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException

from django.core.files import File
from django.utils.translation import gettext as _

from pandas import read_excel
from pandas import to_datetime

class HolidayImporter(BaseEventImporter):
    DATE_COLUMN = 'data'
    NAME_COLUMN = 'nome'

    def __init__(self, file: File, organization: Organization, **kwargs) -> None:
        self.df = read_excel(file, parse_dates=True, header=0)

        self.event_label = Event.HOLIDAY
        self.campi = []
        self.organization = organization

        columns = self.df.columns
        
        if not(self.DATE_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the date column'))
        
        if not(self.NAME_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the name column'))

        if "event_label" in kwargs:
            self.event_label = kwargs["event_label"]

        if "campi" in kwargs:
            self.campi = kwargs["campi"]

        self.df[self.DATE_COLUMN] = to_datetime(self.df[self.DATE_COLUMN], 'raise', format='ISO8601')
        
        super().__init__()

    def import_event(self) -> list:
        events = []
        campi_count = len(self.campi)
        campi_id = [campus.id for campus in self.campi]
        
        for i, row in self.df.iterrows():
            event = Event(start_date=row[self.DATE_COLUMN].date(), description=row[self.NAME_COLUMN])
            event.label = self.event_label
            event.organization = self.organization
            event.save()

            if campi_count > 0:
                event.campi.add(*campi_id)
            
            events.append(event)

        return events