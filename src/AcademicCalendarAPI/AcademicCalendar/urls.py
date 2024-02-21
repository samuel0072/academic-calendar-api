from django.urls import path

from AcademicCalendar.views import *

app_name = 'AcademicCalendar'

urlpatterns = [
    path('calendar/create', academic_calendar_crud.create_calendar, name='create_calendar'),
    path('event/create', event_crud.create_event, name='create_event'),
    path('calendar/<int:id>/events', event_crud.list_event, name='list_calendar_events'),
    path('<int:id>/school_days_count', academic_calendar_crud.school_days_count, name='school_days_count'),
    path('semester/create', semester.create_semester, name='create_semester'),
    path('search_calendar', academic_calendar_crud.search_calendar, name='search_calendar'),
    path('import_regional_holidays', event_crud.import_regional_holidays, name='import_regional_holidays'),
    path('import_national_holidays', event_crud.import_national_holidays, name='import_national_holidays')
]