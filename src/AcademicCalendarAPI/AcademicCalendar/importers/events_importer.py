import datetime
import math

from .base_importer import BaseEventImporter
from AcademicCalendar.models import Event, Organization, AcademicCalendar
from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException

from pandas import read_excel, to_datetime, NaT, to_numeric, NA

from django.core.files import File
from django.utils.translation import gettext as _

class EventsImporter(BaseEventImporter):
    def __init__(self, file: File, organization: Organization, academic_calendar: AcademicCalendar,**kwargs) -> None:
        self.df = read_excel(file, parse_dates=True, header=0)

        self.organization = organization
        self.academic_calendar = academic_calendar

        self.START_DATE_COLUMN  = "data_inicio" if not("start_date_column" in kwargs) else kwargs["start_date_column"]
        self.DESCRIPTION_COLUMN = "descricao" if not("description_column" in kwargs) else kwargs["description_column"]
        self.DURATION_COLUMN    = "duracao" if not("duration_column" in kwargs) else kwargs["duration_column"]
        self.PERIOD_COLUMN      = "espaco" if not("period_column" in kwargs) else kwargs["period_column"]
        self.END_DATE_COLUMN    = "data_fim" if not("end_date_column" in kwargs) else kwargs["end_date_column"]

        columns = self.df.columns
        
        if not(self.START_DATE_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the start date column'))
        
        if not(self.DESCRIPTION_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the description column'))
        
        if not(self.DURATION_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the duration column'))
        
        if not(self.PERIOD_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the period column'))
        
        if not(self.END_DATE_COLUMN in columns):
            raise AcademicCalendarException(_('Could not find the end date column'))

        self.df[self.START_DATE_COLUMN] = to_datetime(self.df[self.START_DATE_COLUMN], 'coerce', format='ISO8601')
        self.df[self.END_DATE_COLUMN] = to_datetime(self.df[self.END_DATE_COLUMN], 'coerce', format='ISO8601')
        self.df[self.DURATION_COLUMN] = to_numeric(self.df[self.DURATION_COLUMN], 'coerce', 'integer')
        self.df[self.PERIOD_COLUMN] = to_numeric(self.df[self.PERIOD_COLUMN], 'coerce', 'integer')
        
        super().__init__()

    def import_event(self):
        
        events = []
        last_period = math.nan
        last_end_date = NaT

        for i, row in self.df.iterrows():
            is_start_date_null = row[self.START_DATE_COLUMN] is NaT
            is_end_date_null = row[self.END_DATE_COLUMN] is NaT

            print(is_end_date_null, row[self.DURATION_COLUMN])

            if is_start_date_null and math.isnan(last_period) :
                raise AcademicCalendarException(_('Could not import row %(row_index)s. '\
                                                  'The start_date_column value must not be empty when the previous row\'s '\
                                                  'period_column value is empty' % {"row_index": i + 1}))
            
            if is_end_date_null and math.isnan(row[self.DURATION_COLUMN]) :
                raise AcademicCalendarException(_('Could not import row %(row_index)s. '\
                                                  'The end_date_column value must not be empty when the row\'s '\
                                                  'duration_column value is empty' % {"row_index": i + 1}))

            event = Event()
            event.description = row[self.DESCRIPTION_COLUMN]
            event.label = Event.SCHOOL_DAYS
            event.academic_calendar = self.academic_calendar
            event.organization = self.organization

            if is_start_date_null:
                event.start_date = last_end_date + datetime.timedelta(days = last_period) 
            else:
                event.start_date = row[self.START_DATE_COLUMN].date()

            last_period = row[self.PERIOD_COLUMN]

            if is_end_date_null:
                event.end_date = event.start_date + datetime.timedelta(days = (row[self.DURATION_COLUMN] - 1)) # menos 1 pois a data inicial também conta na duração
            else:
                event.end_date = row[self.END_DATE_COLUMN].date()
        
            last_end_date = event.end_date

            events.append(event)

        for event in events:
            event.save()

        return events
