from AcademicCalendar.models import TimeStampedModel
from AcademicCalendar.models.Organization import Organization

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class User(AbstractUser, TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{0} {1}".format(_("User"), self.full_name())