from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

# Create your models here.
class TimeStampedModel(models.Model):
    """
    Essa classe contém campos de timestamps.

    Todos os models com exceção de Usuario vão
    herdar dessa classe.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class Organization(TimeStampedModel):
    name = models.TextField(max_length=150)

    def __str__(self) -> str:
        return self.name

class AcademicCalendar(TimeStampedModel):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True, max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.organization.name + ' - ' + self.description
    
class Campus(TimeStampedModel):
    name = models.TextField(max_length=150)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name


class Event(TimeStampedModel):
    HOLIDAY = "H"
    REGIONAL_HOLIDAY = "RH"
    NONSCHOOL_SATURDAY = "NSS"
    NONSCHOOL_DAYS = "NSD"
    SCHOOL_DAYS = "SD"
    LABEL_TYPES = [
        (HOLIDAY, _("Holiday")),
        (REGIONAL_HOLIDAY, _("Regional holiday")),
        (NONSCHOOL_SATURDAY, _("Non-school Saturday")),
        (NONSCHOOL_DAYS, _("Non-school days")), 
        (SCHOOL_DAYS, _("School days"))
    ]

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    label = models.CharField(max_length=3, choices=LABEL_TYPES)
    hexadecimal_color = models.TextField(max_length=6, default="FFFFFF")
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    campi = models.ManyToManyField(Campus, related_name='special_date_campus', blank=True)

    def __str__(self) -> str:
        return self.description + " " + self.get_label_display() 
    
class Semester(TimeStampedModel):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=150)
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.description + ' - ' + self.academic_calendar.__str__()

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{0} {1}".format(_("User"), self.full_name())