import sys
import json
from json.decoder import JSONDecodeError

from AcademicCalendar.models import *
from AcademicCalendar.serializers import *
from AcademicCalendar.importers.holiday_importer import HolidayImporter
from AcademicCalendar.importers.events_importer import EventsImporter
from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException

from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.utils.translation import gettext as _


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_event(request):
    data = request.data
    data['organization'] = request.user.organization.id
    serializer = EventSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])    
def list_events(request, id):
    #busca exata por calendário acadêmico
    serializer = None
    try:
        parsed_id = int(id)

        if(parsed_id > sys.maxsize):
            raise Exception(_("The passed id is not valid"))
        
        events = Event.objects.filter(organization = request.user.organization, academic_calendar__id=parsed_id).order_by('start_date')

        serializer = EventSerializer(data = events, many=True)
        serializer.is_valid()

    except Exception as e:
        return Response({"errors": e.args}, status=status.HTTP_400_BAD_REQUEST, content_type="aplication/json")
    
    return Response(serializer.data, status=status.HTTP_200_OK, content_type="aplication/json")

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])    
def import_regional_holidays(request):
    try:
        if not("campi" in request.data):
            raise AcademicCalendarException(_("campi is required"))
        
        campi = json.loads(request.data["campi"])
        
        if type(campi) != list:
            raise AcademicCalendarException(_("campi should be an array of campus's ids"))
        
        if len(request.FILES) == 0:
            raise AcademicCalendarException(_('No file were provided.'))
        
        if not("file" in request.FILES):
            raise AcademicCalendarException(_('The \'file\' parameter is required.'))
        
        if len(request.FILES) > 1:
            raise AcademicCalendarException(_('You should provide one file at a time'))
        
        campi = Campus.objects.filter(id__in = campi, organization = request.user.organization)

        if len(campi) == 0:
            raise AcademicCalendarException(_('You should provide at least 1 campus from your organization.'))

        importer = HolidayImporter(request.FILES["file"], request.user.organization, campi = campi, event_label=Event.REGIONAL_HOLIDAY)
        imported_events = importer.import_event()

        serializer = EventSerializer(data = imported_events, many=True)
        serializer.is_valid()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, content_type="aplication/json")

    except JSONDecodeError:
        return Response({"errors": _("campi should be a valid json list")}, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except AcademicCalendarException as err:
        return Response({"errors": err.args }, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except ValueError:
        error = _('This file could not be imported. Verify whether the file format is .xlsx or the data is structured in a date, name format.')
        return Response({"errors": [error]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": _('An unexpected error ocurred.')},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
def import_national_holidays(request):
    try:
        if len(request.FILES) == 0:
            raise AcademicCalendarException(_('No file were provided.'))
        
        if not("file" in request.FILES):
            raise AcademicCalendarException(_('The \'file\' parameter is required.'))
        
        if len(request.FILES) > 1:
            raise AcademicCalendarException(_('You should provide one file at a time'))
        
        importer = HolidayImporter(request.FILES["file"], request.user.organization)
        imported_events = importer.import_event()

        serializer = EventSerializer(data = imported_events, many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_201_CREATED, content_type="aplication/json")

    except AcademicCalendarException as err:
        return Response({"errors": err.args }, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except ValueError:
        error = _('This file could not be imported. Verify whether the file format is .xlsx or the data is structured in a date, name format.')
        return Response({"errors": [error]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except Exception as err:
        print(err.args)
        print(type(err))
        return Response({"errors": [_('An unexpected error ocurred.')]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
def import_events(request):
    try:
        if not("academic_calendar_id" in request.data):
            raise AcademicCalendarException(_("The academic calendar id field is required"))
        
        parsed_id = int(request.data["academic_calendar_id"])

        if(parsed_id > sys.maxsize):
            raise Exception(_("The passed id is not valid"))
        
        if len(request.FILES) == 0:
            raise AcademicCalendarException(_('No file were provided.'))
        
        if not("file" in request.FILES):
            raise AcademicCalendarException(_('The \'file\' parameter is required.'))
        
        if len(request.FILES) > 1:
            raise AcademicCalendarException(_('You should provide one file at a time'))
        
        academic_calendar = AcademicCalendar.objects.filter(id = parsed_id, organization = request.user.organization).first()

        if academic_calendar is None:
            raise AcademicCalendarException(_('Could not find the academic calendar.'))

        importer = EventsImporter(request.FILES["file"], request.user.organization, academic_calendar)
        imported_events = importer.import_event()

        serializer = EventSerializer(data = imported_events, many=True)
        serializer.is_valid()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, content_type="aplication/json")
    
    except AcademicCalendarException as err:
        return Response({"errors": err.args }, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except ValueError as err:
        print(err.args)
        error = _('This file could not be imported. Verify if the file format is .xlsx.')
        return Response({"errors": [error]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": _('An unexpected error ocurred.')},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")