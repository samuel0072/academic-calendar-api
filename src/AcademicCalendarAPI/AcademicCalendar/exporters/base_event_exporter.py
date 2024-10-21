from django.db.models import QuerySet
from .base_exporter import BaseExporter

from AcademicCalendar.models import Organization, Event

import pandas

class BaseEventExporter(BaseExporter):
    def __init__(self, organization: Organization, events: QuerySet[Event],**kwargs) -> None:
        self.df = None
        self.organization = organization
        self.events_queryset = events
        self.event_file = None

        self.START_DATE_COLUMN  = "data_inicio" if not("start_date_column" in kwargs) else kwargs["start_date_column"]
        self.DESCRIPTION_COLUMN = "descricao" if not("description_column" in kwargs) else kwargs["description_column"]
        self.END_DATE_COLUMN    = "data_fim" if not("end_date_column" in kwargs) else kwargs["end_date_column"]
        self.LABEL_COLUMN    = "tipo" if not("label_column" in kwargs) else kwargs["label_column"]
        self.CAMPI_COLUMN    = "campi" if not("campi_column" in kwargs) else kwargs["campi_column"]

    def construct_df(self):
        #fazer um loop pelo events queryset, se não funcionar, trocar o BaseManager[Event] por um queryset
        data = []
        for event in self.events_queryset:
            campi = event.campi.all()

            campi_str = "| " if len(campi) > 0 else ""

            for campus in campi:
                campi_str += ( campus.name + " | " )
            
            data.append( (event.start_date, event.description, event.end_date, event.get_label_display(), campi_str ) )

        self.df = pandas.DataFrame.from_records(data, columns=[self.START_DATE_COLUMN, self.DESCRIPTION_COLUMN, self.END_DATE_COLUMN, self.LABEL_COLUMN, self.CAMPI_COLUMN])
        self.df[self.START_DATE_COLUMN] = pandas.to_datetime(self.df[self.START_DATE_COLUMN], errors='coerce')
        self.df[self.END_DATE_COLUMN] = pandas.to_datetime(self.df[self.END_DATE_COLUMN], errors='coerce')
    
    def export(self):
        pass
