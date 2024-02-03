import sys
from AcademicCalendar.models import *
from AcademicCalendar.serializers import *
from AcademicCalendar.utils import count_school_days

from django.http import JsonResponse
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

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
        parsed_id = int(id)

        if(parsed_id > sys.maxsize):
            raise Exception(_("The passed id is not valid"))
        
        calendar = AcademicCalendar.objects.filter(id=parsed_id, organization__id = request.user.organization.id).get()

        response_data = count_school_days(calendar)
        return Response(response_data, status=status.HTTP_200_OK, content_type="aplication/json")

    except Exception as e:
        return Response({"errors": e.args}, status=status.HTTP_400_BAD_REQUEST, content_type="aplication/json")
    
    