from AcademicCalendar.models import *
from AcademicCalendar.serializers import *

from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createCalendar(request):
    data = request.data
    data['organization'] = request.user.organization.id
    serializer = CalendarSerializer(data = data)
    if serializer.is_valid():
        calendar = serializer.save()

        if(calendar.description is None or len(calendar.description) == 0):
            calendar.description = "Calendário Acadêmico " + str(calendar.id)
            calendar.save()
        serializer = CalendarSerializer(calendar)   

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)