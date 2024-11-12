from AcademicCalendar.models import TimeStampedModel
from AcademicCalendar.models.Organization import Organization

from django.db import models
from django.utils.translation import gettext as _

class EventFile(TimeStampedModel):
    TYPE_CSV = ".csv"
    TYPE_EXCEL = ".xlsx"
    TYPE_PDF = ".pdf"

    LABEL_TYPES = [
        (TYPE_CSV, _("CSV")),
        (TYPE_EXCEL, _("EXCEL")),
        (TYPE_PDF, _("PDF"))
    ]

    file_path =  models.TextField(max_length=500, blank=True, null=True)
    format = models.CharField(max_length=5, choices=LABEL_TYPES)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self):
        return "{0} - {1}".format(self.get_format_display(), self.file_path)