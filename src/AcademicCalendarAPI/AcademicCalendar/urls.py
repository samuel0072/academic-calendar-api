from django.urls import path

from AcademicCalendar.views import *

app_name = 'AcademicCalendar'

urlpatterns = [
    path('calendar/detail/<int:id>', academic_calendar_crud.get_calendar_detail, name='get_calendar_detail'),
    path('calendar/create', academic_calendar_crud.create_calendar, name='create_calendar'),
    path('event/create', event_crud.create_event, name='create_event'),
    path('calendar/<int:id>/events', event_crud.list_events, name='list_calendar_events'),
    path('calendar/<int:id>/semesters', semester.list_semesters, name='list_calendar_semesters'),
    #falta uma rota de listar feriados nacionais e regionais da organização
    path('calendar/<int:id>/export/csv', academic_calendar_crud.export_academic_calendar_events_to_csv, name='export_academic_calendar_events_to_csv'),
    path('calendar/<int:id>/export/excel', academic_calendar_crud.export_academic_calendar_events_to_excel, name='export_academic_calendar_events_to_excel'),
    path('<int:id>/school_days_count', academic_calendar_crud.school_days_count, name='school_days_count'),
    path('semester/create', semester.create_semester, name='create_semester'),
    path('search_calendar', academic_calendar_crud.search_calendar, name='search_calendar'),
    path('import_regional_holidays', event_crud.import_regional_holidays, name='import_regional_holidays'),
    path('import_national_holidays', event_crud.import_national_holidays, name='import_national_holidays'),
    path('calendar/<int:id>/import_events', event_crud.import_events, name='import_events'),
    path('event/<int:id>/edit', event_crud.edit_event, name='edit_event'),
    path('event/<int:id>/delete', event_crud.delete_event, name='delete_event'),
    path('semester/<int:id>/edit', semester.edit_semester, name='edit_semester'),
    path('semester/<int:id>/delete', semester.delete_semester, name='delete_semester'),
    path('semester/<int:id>', semester.get_semester_detail, name='get_semester_detail'),
    path('campus/create', campus.create_campus, name='create_campus'),
    path('campus/list', campus.list_campus, name='list_campus'),
    path('campus/<int:id>/edit', campus.edit_campus, name='edit_campus'),
    path('campus/<int:id>/delete', campus.delete_campus, name='delete_campus'),
    path('event_file/<int:id>/download/', academic_calendar_crud.download_event_file, name='download_event_file'),
    path('user/create', user.create_user, name='create_user'),
    path('user/profile', user.profile, name='user_profile'),
]