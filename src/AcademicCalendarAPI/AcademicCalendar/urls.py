from django.urls import path, include

from AcademicCalendar.views import *

app_name = 'AcademicCalendar'

urlpatterns = [
    path('create', academic_calendar_crud.createCalendar, name='createCalendar')
]