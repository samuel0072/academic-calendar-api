import datetime

class DaysCounterHelper:
    SUNDAY_WEEK_DAY = 6
    SATURDAY_WEEK_DAY = 5
    FRIDAY_WEEK_DAY = 4
    THURSDAY_WEEK_DAY = 3
    WEDNESDAY_WEEK_DAY = 2
    TUESDAY_WEEK_DAY = 1
    MONDAY_WEEK_DAY = 0
    
    @staticmethod
    def allDatesSpecificWeekDay(weekday: int, start_date: datetime.date, end_date: datetime.date):
        """
            Retorna todas as datas que um dia específico da semana ocorre durante um determinado período
        """
        days = []
        actual_date = start_date + datetime.timedelta(days=weekday - start_date.weekday())

        while( actual_date <= end_date ):
            days.append(actual_date)
            actual_date += datetime.timedelta(days=7)
        
        return days
    
    @staticmethod
    def allDaysIn(start_date: datetime.date, end_date: datetime.date, week_ex_day = []):
        """
            Retorna todas as datas durante um determinado período
        """
        days = []
        actual_date = start_date

        while( actual_date <= end_date ):
            if actual_date.weekday() not in week_ex_day:
                days.append(actual_date)
            actual_date += datetime.timedelta(days=1)
        
        return days