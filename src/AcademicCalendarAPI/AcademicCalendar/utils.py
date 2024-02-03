from .models import *
import datetime

SUNDAY_WEEK_DAY = 6

def count_school_days(calendar: AcademicCalendar) -> dict:
    counting = {"total_days": 0, "sundays": 0, "school_days" : 0}
    total_days = (calendar.end_date - calendar.start_date).days + 1

    sundays_count = count_specific_weekdays_between_two_dates(SUNDAY_WEEK_DAY, calendar.start_date, calendar.end_date)

    counting["total_days"] = total_days
    counting["sundays"] = sundays_count
    counting["school_days"] = total_days - sundays_count

    return counting

def count_specific_weekdays_between_two_dates(weekday: int, start_date: datetime.date, end_date: datetime.date) -> int:
    weekday_count = 0
    actual_date = start_date + datetime.timedelta(days=weekday - start_date.weekday())

    while( actual_date <= end_date ):
        weekday_count += 1
        actual_date += datetime.timedelta(days=7)
    
    return weekday_count