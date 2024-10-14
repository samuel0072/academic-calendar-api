from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext as _

from AcademicCalendar.services.Organization import OrganizationService

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def get_org_info(request):
    service = OrganizationService(request.user)

    return Response(service.getOrgInfo(), status=status.HTTP_200_OK, content_type="aplication/json")

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  
def update_minutes_info(request):
    service = OrganizationService(request.user)

    try:
        org_data = service.updateMinutesInfo(request.data)
        return Response(org_data, status=status.HTTP_200_OK, content_type="aplication/json")
    
    except ValidationError as e:
        return Response(e.args[0], status=status.HTTP_422_UNPROCESSABLE_ENTITY, content_type="aplication/json")