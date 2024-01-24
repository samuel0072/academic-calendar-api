from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Organization)
admin.site.register(AcademicCalendar)
admin.site.register(Event)
admin.site.register(Campus)
admin.site.register(SpecialDate)
admin.site.register(Semester)
admin.site.register(User)