from django.db.models import QuerySet
from AcademicCalendar.models import Event, Organization, EventFile
from .base_event_exporter import BaseEventExporter
from django.conf import settings

class CSVEventExporter(BaseEventExporter):
    def __init__(self, organization: Organization, events: QuerySet[Event], **kwargs) -> None:
        super().__init__(organization, events, **kwargs)

    def export(self):
        event_file = EventFile(format = EventFile.TYPE_CSV, organization = self.organization)

        event_file.save()

        event_file.file_path = "{0}/{1}{2}{3}".format(settings.BASE_DIR, settings.MEDIA_ROOT, event_file.id, event_file.format)

        self.df.to_csv(event_file.file_path, date_format = "%d/%m/%Y", index=False)

        event_file.save()
