from .models import *
import datetime

SUNDAY_WEEK_DAY = 6

def count_school_days(calendar: AcademicCalendar) -> dict:
    counting = {"total_days": 0, "sundays": 0}
    sem= {}
    total_days = (calendar.end_date - calendar.start_date).days + 1

    sundays_count = count_specific_weekdays_between_two_dates(SUNDAY_WEEK_DAY, calendar.start_date, calendar.end_date)

    semesters = Semester.objects.filter(academic_calendar = calendar)

    counting["total_days"] = total_days
    counting["sundays"] = sundays_count

    for semester in semesters:
        sem[semester.description] = count_non_school_days_semester(semester)
    
    counting["semesters"] = sem

    return counting

def count_specific_weekdays_between_two_dates(weekday: int, start_date: datetime.date, end_date: datetime.date) -> int:
    weekday_count = 0
    actual_date = start_date + datetime.timedelta(days=weekday - start_date.weekday())

    while( actual_date <= end_date ):
        weekday_count += 1
        actual_date += datetime.timedelta(days=7)
    
    return weekday_count

def count_non_school_days_semester(semester: Semester) -> int:
    non_school_days = {}
    campi = Campus.objects.filter(organization = semester.organization)
    
    semester_total_days = (semester.end_date - semester.start_date).days + 1
    sundays_count = count_specific_weekdays_between_two_dates(SUNDAY_WEEK_DAY, semester.start_date, semester.end_date)
    available_school_days = semester_total_days - sundays_count
    
    for campus in campi:
        campus_non_school_day = non_school_days_in_campus(campus, semester.start_date, semester.end_date)
        non_school_days[campus.id] = available_school_days - len(campus_non_school_day)
    
    return non_school_days

def non_school_days_in_campus(campus: Campus, start_date: datetime.date, end_date: datetime.date) -> set:
    non_school_days = []
    campus_non_school_events = Event.objects.filter(campi__id = campus.id, start_date__gte = start_date, end_date__lte = end_date).exclude(label=Event.SCHOOL_DAYS)
    national_holidays = Event.objects.filter(
        start_date__gte = start_date, 
        end_date__lte = end_date, 
        label=Event.HOLIDAY, 
        organization = campus.organization
        )
    non_school_days_qs = campus_non_school_events.union(national_holidays)

    for event in non_school_days_qs:
        non_school_days += non_school_days_in(event.start_date, event.end_date)
    
    return set(non_school_days)

def non_school_days_in(start_date: datetime.date, end_date: datetime.date) -> []:
    days = []
    actual_date = start_date

    while( actual_date <= end_date ):
        if actual_date.weekday() != SUNDAY_WEEK_DAY:
            days.append(actual_date)
        actual_date += datetime.timedelta(days=1)
    
    return days