from  AcademicCalendar.models import Event
from AcademicCalendar.helpers.DaysCounterHelper import DaysCounterHelper
from AcademicCalendar.services.BaseService import BaseService

class CampusService(BaseService): 
        def schoolDaysSummaryForAcademicCalendar(self, calendar, campus, start_date, end_date):
            """
                Retorna um set com todas as datas que são dias letivos no campus para o calendário
            """

            available_days = set(DaysCounterHelper.allDaysIn(start_date, end_date))

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
            
            saturday_school_day = Event.objects.filter(
                label = Event.SCHOOL_SATURDAY,
                campi__id = campus.id, 
                academic_calendar = calendar,
                start_date__gte = start_date, 
                end_date__lte = end_date, 
                deleted_at__isnull = True)
            
            non_school_days_qs = campus_non_school_events.union(national_holidays.union(regional_holidays))

            school_saturday_set = set()

            for event in non_school_days_qs:
                non_school_days += DaysCounterHelper.allDaysIn(event.start_date, event.end_date)

            non_school_days = set(non_school_days)

            for saturday in saturday_school_day:
                school_saturday_set.add(saturday.start_date)

            #remove os sábados letivos, mas que possuem algum evento não letivo
            school_saturday_set = school_saturday_set.difference(non_school_days)

            #remove todos os domingos, sábados e eventos não letivos
            sundays = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.SUNDAY_WEEK_DAY, start_date, end_date)
            saturdays = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.SATURDAY_WEEK_DAY, start_date, end_date)

            available_days = available_days.difference(sundays)
            available_days = available_days.difference(saturdays)
            available_days = available_days.difference(non_school_days)

            #readiciona os sábados que são sábados letivos restantes
            available_days = available_days.union(school_saturday_set)

            return available_days
        
        def getWeekDays(self, available_days: set, start, end):
            monday = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.MONDAY_WEEK_DAY, start, end)
            tuesday = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.TUESDAY_WEEK_DAY, start, end)
            wednesday = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.WEDNESDAY_WEEK_DAY, start, end)
            thursday = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.THURSDAY_WEEK_DAY, start, end)
            friday = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.FRIDAY_WEEK_DAY, start, end)
            saturday = DaysCounterHelper.allDatesSpecificWeekDay(DaysCounterHelper.SATURDAY_WEEK_DAY, start, end)

            return {
                "monday": len(available_days.intersection(monday)),
                "tuesday": len(available_days.intersection(tuesday)),
                "wednesday": len(available_days.intersection(wednesday)),
                "thursday": len(available_days.intersection(thursday)),
                "friday": len(available_days.intersection(friday)),
                "saturday": len(available_days.intersection(saturday))
            }