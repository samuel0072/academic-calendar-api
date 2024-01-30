from AcademicCalendar.models import *
from AcademicCalendar.serializers import *
from django.utils.translation import gettext as _

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_special_date(request):
    
    data = request.data

    data["organization"] = request.user.organization.id

    serializer = SpecialDateSerializer(data = data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK, content_type="aplication/json")
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")
    
    