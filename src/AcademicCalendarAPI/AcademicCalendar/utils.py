from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException
import sys
from .models import *
import datetime

from django.utils.translation import gettext as _

SUNDAY_WEEK_DAY = 6
SATURDAY_WEEK_DAY = 5

def count_school_days(calendar: AcademicCalendar):
    counting = {"total_days": 0, "sundays": 0}
    sem= {}
    total_days = (calendar.end_date - calendar.start_date).days + 1

    sundays_count = len(specific_weekdays_between_two_dates(SUNDAY_WEEK_DAY, calendar.start_date, calendar.end_date))
    saturdays_count = len(specific_weekdays_between_two_dates(SATURDAY_WEEK_DAY, calendar.start_date, calendar.end_date))

    semesters = Semester.objects.filter(academic_calendar = calendar, deleted_at__isnull = True)

    counting["total_days"] = total_days
    counting["saturday"] = saturdays_count
    counting["sundays"] = sundays_count

    sem = []
    for semester in semesters:
        sem.append({ "description": semester.description, "campi_school_days_count":  count_non_school_days_semester(semester)})
        #sem[semester.description] = count_non_school_days_semester(semester)
    
    counting["semesters"] = sem

    return counting

def specific_weekdays_between_two_dates(weekday: int, start_date: datetime.date, end_date: datetime.date):
    days = []
    actual_date = start_date + datetime.timedelta(days=weekday - start_date.weekday())

    while( actual_date <= end_date ):
        days.append(actual_date)
        actual_date += datetime.timedelta(days=7)
    
    return days


def count_non_school_days_semester(semester: Semester):
    campi = Campus.objects.filter(organization = semester.organization, deleted_at__isnull = True)
    
    semester_total_days = (semester.end_date - semester.start_date).days + 1

    #por padrão, sábado e domingo não conta
    sundays = specific_weekdays_between_two_dates(SUNDAY_WEEK_DAY, semester.start_date, semester.end_date)
    saturdays = specific_weekdays_between_two_dates(SATURDAY_WEEK_DAY, semester.start_date, semester.end_date)

    available_school_days = semester_total_days - len(sundays) - len(saturdays)
    
    campi_school_days = []
    for campus in campi:
        campus_non_school_day = non_school_days_in_campus(campus, semester.academic_calendar, semester.start_date, semester.end_date)

        #obtem todos os sábados letivos
        saturday_school_days_events = saturday_school_days_in_campus(campus, semester.academic_calendar, semester.start_date, semester.end_date)

        #porém se houver algum outro evento não letivo no sábado, o sábado em questão não é levado em conta
        sat_school_days = [day for day in saturday_school_days_events if day not in campus_non_school_day ]

        campus_school_days_without_saturdays = [ day for day in  campus_non_school_day if day not in saturdays ]

        school_days_count = available_school_days + len(sat_school_days)  - len(campus_school_days_without_saturdays)

        campi_school_days.append({ "id": campus.id, "name": campus.name, "school_days_count": school_days_count })
    
    return campi_school_days

def non_school_days_in_campus(campus: Campus, calendar:AcademicCalendar, start_date: datetime.date, end_date: datetime.date):
    non_school_days = []
    
    campus_non_school_events =  Event.objects.filter(
        label = Event.NONSCHOOL_DAYS,
        academic_calendar = calendar,
        campi__id = campus.id, 
        start_date__gte = start_date, 
        end_date__lte = end_date, 
        deleted_at__isnull = True)
    
    national_holidays = Event.objects.filter(
        start_date__gte = start_date, 
        end_date__lte = end_date, 
        label=Event.HOLIDAY, 
        organization = campus.organization,
        deleted_at__isnull = True
    )

    regional_holidays =  Event.objects.filter(
        label = Event.REGIONAL_HOLIDAY,
        campi__id = campus.id, 
        start_date__gte = start_date, 
        end_date__lte = end_date, 
        deleted_at__isnull = True)
    
    non_school_days_qs = campus_non_school_events.union(national_holidays.union(regional_holidays))

    for event in non_school_days_qs:
        non_school_days += week_days_in(event.start_date, event.end_date)
    
    return set(non_school_days)

def saturday_school_days_in_campus(campus: Campus, calendar:AcademicCalendar, start_date: datetime.date, end_date: datetime.date):
    school_days = []
    qs =  Event.objects.filter(
        label = Event.SCHOOL_SATURDAY,
        academic_calendar = calendar,
        campi__id = campus.id, 
        start_date__gte = start_date, 
        end_date__lte = end_date, 
        deleted_at__isnull = True)
    
    for event in qs:
        school_days += week_days_in(event.start_date, event.end_date)
    
    return set(school_days)

def week_days_in(start_date: datetime.date, end_date: datetime.date, week_ex_day = [SUNDAY_WEEK_DAY]):
    days = []
    actual_date = start_date

    while( actual_date <= end_date ):
        if actual_date.weekday() not in week_ex_day:
            days.append(actual_date)
        actual_date += datetime.timedelta(days=1)
    
    return days

def validate_id(id) -> int:
    parsed_id = int(id)

    if(parsed_id > sys.maxsize):
        raise AcademicCalendarException(_("The passed id is not valid"))
    
    return parsed_id