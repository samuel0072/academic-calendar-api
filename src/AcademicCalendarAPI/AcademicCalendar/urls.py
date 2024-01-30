from django.urls import path

from AcademicCalendar.views import *

app_name = 'AcademicCalendar'

urlpatterns = [
    path('calendar/create', academic_calendar_crud.create_calendar, name='create_calendar'),
    path('event/create', event_crud.create_event, name='create_event'),
    path('calendar/<int:id>/events', event_crud.list_event, name='list_calendar_events'),
    path('special_date/create', special_date_crud.create_special_date,  name='create_special_date')
]