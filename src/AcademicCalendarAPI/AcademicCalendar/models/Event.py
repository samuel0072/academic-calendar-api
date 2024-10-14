from AcademicCalendar.models.TimeStampedModel import TimeStampedModel
from AcademicCalendar.models.Organization import Organization
from AcademicCalendar.models.AcademicCalendar import AcademicCalendar
from AcademicCalendar.models.Campus import Campus

from django.db import models
from django.utils.translation import gettext as _

class Event(TimeStampedModel):
    HOLIDAY = "H"
    REGIONAL_HOLIDAY = "RH"
    SCHOOL_SATURDAY = "SS"
    NONSCHOOL_DAYS = "NSD"
    SCHOOL_DAYS = "SD"
    LABEL_TYPES = [
        (HOLIDAY, _("National holiday")),
        (REGIONAL_HOLIDAY, _("Regional holiday")),
        (SCHOOL_SATURDAY, _("School saturday")),
        (NONSCHOOL_DAYS, _("Non-school days")), 
        (SCHOOL_DAYS, _("School days"))
    ]

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    label = models.CharField(max_length=3, choices=LABEL_TYPES)
    hexadecimal_color = models.TextField(max_length=7, default="#FFFFFF")
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.PROTECT, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    campi = models.ManyToManyField(Campus, related_name='special_date_campus', blank=True)

    def __str__(self) -> str:
        return self.description + " " + self.get_label_display() 