from django.db.models import QuerySet
from AcademicCalendar.models import Event, Organization, EventFile
from .base_event_exporter import BaseEventExporter
from django.conf import settings
from django.urls import reverse

class CSVEventExporter(BaseEventExporter):
    def __init__(self, organization: Organization, events: QuerySet[Event], **kwargs) -> None:
        super().__init__(organization, events, **kwargs)

    def export(self):
        self.construct_df()

        self.event_file = EventFile(format = EventFile.TYPE_CSV, organization = self.organization)

        self.event_file.save()

        self.event_file.file_path = "{0}{1}".format(self.event_file.id, self.event_file.format)

        self.df.to_csv("{0}/{1}{2}".format(settings.BASE_DIR, settings.MEDIA_ROOT, self.event_file.file_path), date_format = "%d/%m/%Y", index=False)

        self.event_file.save()

        self.file_url = reverse("academic_calendar:download_event_file", args=(self.event_file.id, ))
