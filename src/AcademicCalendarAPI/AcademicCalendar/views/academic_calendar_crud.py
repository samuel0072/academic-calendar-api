from AcademicCalendar.models import *
from AcademicCalendar.serializers import *

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def createCalendar(request):
    serializer = CalendarSerializer(data = request.data)
    if serializer.is_valid():
        calendar = serializer.save()

        if(calendar.description is None or len(calendar.description) == 0):
            calendar.description = "Calendário Acadêmico " + str(calendar.id)

        serializer = CalendarSerializer(calendar)

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)