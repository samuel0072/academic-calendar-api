from django.db.models import QuerySet
from AcademicCalendar.models import Event, Organization, EventFile
from .base_event_exporter import BaseEventExporter
from django.conf import settings

class CSVEventExporter(BaseEventExporter):
    def __init__(self, organization: Organization, events: QuerySet[Event], **kwargs) -> None:
        super().__init__(organization, events, **kwargs)

    def export(self):
        self.construct_df()

        self.event_file = EventFile(format = EventFile.TYPE_CSV, organization = self.organization)

        self.event_file.save()

        self.event_file.file_path = "{0}/{1}{2}{3}".format(settings.BASE_DIR, settings.MEDIA_ROOT, self.event_file.id, self.event_file.format)

        self.df.to_csv(self.event_file.file_path, date_format = "%d/%m/%Y", index=False)

        self.event_file.save()
