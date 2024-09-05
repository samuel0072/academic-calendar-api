import datetime
from AcademicCalendar.models import *
from AcademicCalendar.serializers import *
from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException
from AcademicCalendar.utils import validate_id

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from django.utils.translation import gettext as _

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_semester(request):
    data = request.data
    data['organization'] = request.user.organization.id
    serializer = SemesterSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def edit_semester(request, id):
    try:
        parsed_id = validate_id(id)

        semester = Semester.objects.get(pk=parsed_id, organization = request.user.organization, deleted_at__isnull = True)
        
        request.data["organization"] = request.user.organization.id
        
        serializer = SemesterSerializer(semester, data = request.data )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type="aplication/json")
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    except Semester.DoesNotExist:
        return Response({"errors": [_('Could not find the semester.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except AcademicCalendarException as err:
        return Response({"errors": err.args }, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")
    
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def delete_semester(request, id):
    try:
        parsed_id = validate_id(id)

        semester = Semester.objects.get(pk=parsed_id, organization = request.user.organization)
        
        semester.deleted_at = datetime.datetime.now()
        semester.save()   

        return Response(status=status.HTTP_204_NO_CONTENT)
        
    except Semester.DoesNotExist:
        return Response({"errors": [_('Could not find the semester.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])    
def get_semester_detail(request, id):
    try:
        parsed_id = validate_id(id)

        semester = Semester.objects.get(pk=parsed_id, organization = request.user.organization)

        semester_serializer = SemesterSerializer(semester)

        return Response(semester_serializer.data, status=status.HTTP_200_OK, content_type="aplication/json")
        
    except Semester.DoesNotExist:
        return Response({"errors": [_('Could not find the semester.')]},  status=status.HTTP_404_NOT_FOUND, content_type="aplication/json")
    
    except Exception as e:
        print(e.args)
        return Response({"errors": [_('An unexpected error ocurred.')]},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")