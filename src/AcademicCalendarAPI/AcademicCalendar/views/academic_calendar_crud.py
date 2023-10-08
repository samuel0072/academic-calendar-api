from AcademicCalendar.models import *
from AcademicCalendar.serializers import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def createCalendar(request):
    serializer = CalendarSerializer(data = request.data)
    serializer.is_valid()
    calendar = serializer.save()

    serializer = CalendarSerializer(calendar)

    return Response(serializer.data, content_type='aplication/json', status=status.HTTP_201_CREATED)