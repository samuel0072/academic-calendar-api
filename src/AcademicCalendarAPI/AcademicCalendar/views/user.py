from AcademicCalendar.models import *
from AcademicCalendar.serializers import *
from AcademicCalendar.exceptions.academic_calendar_exceptions import AcademicCalendarException

from django.http import JsonResponse
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.utils.translation import gettext as _

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_user(request):
    try:
        data = request.data
        data['organization'] = request.user.organization.id
        data['username'] = request.data['email']

        serializer = UserSerializer(data = data)

        if serializer.is_valid():
            password = request.data["password"]

            if password != request.data["confirm_password"]:
                raise ValidationError([[_('password and confirm_password are not equal.')]])
            
            validators.validate_password(password)

            user = serializer.save()
            user.set_password(password)
            user.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except AcademicCalendarException as err:
        return JsonResponse(err.args, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except ValidationError as err:
        errors = []
        for error in err.args[0]:
            errors.extend(error)

        return JsonResponse({ "password" : errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    except Exception as e:
        print(e.args)
        return Response({"errors": _('An unexpected error ocurred.')},  status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="aplication/json")