from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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

class Event(TimeStampedModel):
    LABEL_TYPES = [
        ('NSD', settings.TRANSLATIONS.NonSchoolDays), 
        ('SD', settings.TRANSLATIONS.SchoolDays)
    ]

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True, max_length=500)
    label = models.CharField(blank=True, null=True, max_length=3, choices=LABEL_TYPES)
    hexadecimal_color = models.TextField(max_length=6, default="FFFFFF")
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.description
    
class Campus(TimeStampedModel):
    name = models.TextField(max_length=150)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name

class SpecialDate(TimeStampedModel):
    SPECIAL_DATE_TYPES = [
        ('H', settings.TRANSLATIONS.Holiday),
        ('RH', settings.TRANSLATIONS.RegionalHoliday),
        ('NSS', settings.TRANSLATIONS.NonSchoolSaturday),
        ('NSD', settings.TRANSLATIONS.NonSchoolDay),
    ]

    date = models.DateField()
    type = models.CharField(blank=True, null=True, max_length=3, choices=SPECIAL_DATE_TYPES)
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.PROTECT, blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    campi = models.ManyToManyField(Campus, related_name='special_date_campus', blank=True)
    description = models.TextField(blank=True, null=True, max_length=500)

    def __str__(self) -> str:
        return self.date.isoformat() + ' - ' + self.description + ' - ' + self.get_type_display() 
    
class Semester(TimeStampedModel):
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    description = models.TextField(max_length=150)
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.description + ' - ' + self.academic_calendar.__str__()

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def full_name(self):
        """
        Retorna o nome completo do usuário
        """
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{0} {1}".format(settings.TRANSLATIONS.User, self.full_name())

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)