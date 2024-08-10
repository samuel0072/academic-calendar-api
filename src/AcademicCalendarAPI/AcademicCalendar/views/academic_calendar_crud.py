import os
from AcademicCalendar.models import *
from AcademicCalendar.serializers import *
from AcademicCalendar.utils import count_school_days, validate_id
from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException
from AcademicCalendar.exporters.csv_event_exporter import CSVEventExporter
from AcademicCalendar.exporters.excel_event_exporter import ExcelEventExporter

from django.http import JsonResponse, FileResponse
from django.utils.translation import gettext as _
from django.conf import settings
from django.urls import reverse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination 

paginator = PageNumberPagination()

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_calendar(request):
    data = request.data
    data['organization'] = request.user.organization.id
    serializer = CalendarSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def school_days_count(request, id):
    
    try:
        parsed_id = validate_id(id)
        
        calendar = AcademicCalendar.objects.get(id=parsed_id, organization__id = request.user.organization.id, deleted_at__isnull = True)

        response_data = count_school_days(calendar)
        return Response(response_data, status=status.HTTP_200_OK, content_type="aplication/json")

    except AcademicCalendarException as err:
        return Response({"errors": err.args }, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except AcademicCalendar.DoesNotExist:
        return Response({"errors": [_('Could not find the academic calendar.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_calendar(request):
    params = CalendarSearchSerializer(data = request.query_params)

    if params.is_valid():
        calendars = AcademicCalendar.objects.filter(organization__id = request.user.organization.id)

        if params.data["id"] != None:
            calendars = calendars.filter(pk = params.data["id"])
        
        if params.data["start_date"] != None:
            calendars = calendars.filter(start_date__gte = params.data["start_date"])
        
        if params.data["end_date"] != None:
            calendars = calendars.filter(start_date__lte = params.data["end_date"])
    
        if params.data["description"] != None:
            calendars = calendars.filter(description__icontains = params.data["description"])

        calendars = calendars.exclude(deleted_at__isnull = False).order_by('updated_at')

        calendar_serializer = CalendarSerializer(data = calendars, many = True)

        calendar_serializer.is_valid()

        return Response(calendar_serializer.data, status=status.HTTP_200_OK, content_type="aplication/json")
    
    return Response(params.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])      
def export_academic_calendar_events_to_csv(request, id):
    try:
        parsed_id = validate_id(id)

        calendar = AcademicCalendar.objects.get(pk=parsed_id, organization = request.user.organization)

        calendar_events = Event.objects.filter(academic_calendar = calendar, organization = request.user.organization)
        holidays = Event.objects.filter(label__in = [Event.HOLIDAY, Event.REGIONAL_HOLIDAY], 
                                        organization = request.user.organization, 
                                        start_date__gte = calendar.start_date, 
                                        start_date__lte = calendar.end_date)
        
        events = calendar_events.union(holidays)
        
        exporter = CSVEventExporter(request.user.organization, events)
        exporter.export()

        response_objects = {
            "url": exporter.file_url
        }

        return Response(response_objects, status=status.HTTP_201_CREATED)
        
    except AcademicCalendar.DoesNotExist:
        return Response({"errors": [_('Could not find the academic calendar.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def download_event_file(request, id):
    try:
        parsed_id = validate_id(id)

        file = EventFile.objects.get(pk=parsed_id, organization = request.user.organization)

        file_path = os.path.join(settings.MEDIA_ROOT, file.file_path)
        
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        
        else:
            raise AcademicCalendarException(_('Could not retrieve the especified file. It may be deleted.'))
        
    except EventFile.DoesNotExist:
        return Response({"errors": [_('Could not find the file.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except AcademicCalendarException as err:
        return Response({"errors": err.args }, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])      
def export_academic_calendar_events_to_excel(request, id):
    try:
        parsed_id = validate_id(id)

        calendar = AcademicCalendar.objects.get(pk=parsed_id, organization = request.user.organization)

        calendar_events = Event.objects.filter(academic_calendar = calendar, organization = request.user.organization)
        holidays = Event.objects.filter(label__in = [Event.HOLIDAY, Event.REGIONAL_HOLIDAY], 
                                        organization = request.user.organization, 
                                        start_date__gte = calendar.start_date, 
                                        start_date__lte = calendar.end_date)
        
        events = calendar_events.union(holidays)
        
        exporter = ExcelEventExporter(request.user.organization, events)
        exporter.export()

        response_objects = {
            "url": exporter.file_url
        }

        return Response(response_objects, status=status.HTTP_201_CREATED)
        
    except AcademicCalendar.DoesNotExist:
        return Response({"errors": [_('Could not find the academic calendar.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])    
def get_calendar_detail(request, id):
    try:
        parsed_id = validate_id(id)

        calendar = AcademicCalendar.objects.get(pk=parsed_id, organization = request.user.organization)

        calendar_serializer = CalendarSerializer(calendar)

        return Response(calendar_serializer.data, status=status.HTTP_200_OK, content_type="aplication/json")
        
    except AcademicCalendar.DoesNotExist:
        return Response({"errors": [_('Could not find the academic calendar.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")