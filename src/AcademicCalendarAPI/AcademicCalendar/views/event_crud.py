import sys
from AcademicCalendar.models import *
from AcademicCalendar.serializers import *

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
def list_event(request, id):
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