from rest_framework import serializers
from .models import *
from django.utils.translation import gettext as _
from django.db.models import Q
import re
import sys

SATURDAY_WEEKDAY = 5

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalendar
        fields = ['id', 'start_date', 'end_date', 'description', 'organization']

    def validate(self, data):
        errors = {}
            
        if(data['end_date'] < data['start_date']):
            errors['end_date'] = _("End date has to be after start date")
            
        if(len(errors) > 0):
            raise serializers.ValidationError(errors)
        
        return data

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 
            'start_date', 
            'end_date', 
            'description', 
            'organization', 
            'label', 
            'hexadecimal_color', 
            'academic_calendar',
            'campi'
        ]

    def validate_hexadecimal_color(self, value):
        if re.search(r"#([0-9a-fA-F]){6}", value) == None:
            raise serializers.ValidationError(_("Color has to be a number in a hexadecimal format"))
        
        return value
    
    def validate(self, data):
        errors = {}
        if len(data['description']) == 0:
            errors['description'] = _("An empty description is not valid")

        if(data['end_date'] < data['start_date']):
           errors['end_date'] = _("End date has to be after start date")
        
        if data["label"] != Event.HOLIDAY and len(data["campi"]) == 0:
            errors['campi'] = _("A campus must be provided for this event")
        
        if (data["label"] == Event.SCHOOL_SATURDAY) and (data['start_date'].weekday() != SATURDAY_WEEKDAY):
            errors['start_date'] = _("This start date isn't a saturday")
        
        if(data["label"] == Event.HOLIDAY):
            data["campi"] = []
        
        if(data["label"] in [Event.HOLIDAY, Event.REGIONAL_HOLIDAY]):
            data["academic_calendar"] = None
            
        if data["academic_calendar"] != None:
            if data["academic_calendar"].organization.id != data["organization"].id:
                errors['academic_calendar'] = _("You don't have permission to create events on this calendar")
            
            if data["academic_calendar"].deleted_at != None:
                errors['academic_calendar'] = _("Could not find the academic calendar.")
        
        for campus in data["campi"]:
            if campus.organization.id != data["organization"].id:
                errors['academic_calendar'] = _("You don't have permission to create events on this campus: %(name)s" % {"name": campus.name} )
            
        if(len(errors) > 0):
            raise serializers.ValidationError(errors)
        
        return data
    
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'id', 
            'start_date', 
            'end_date', 
            'description', 
            'organization', 
            'academic_calendar',
            'lessons_start_date',
            'lessons_end_date'
        ]

    def validate(self, data):
        errors = {}
        if(data['end_date'] < data['start_date']):
           errors['end_date'] = _("End date has to be after start date")

        if(data['lessons_end_date'] < data['lessons_start_date']):
           errors['lessons_end_date'] = _("Lessons end date has to be after lessons start date")

        if( (data['lessons_start_date'] < data['start_date']) or  (data['lessons_start_date'] > data['end_date']) ):
           errors['lessons_start_date'] = _("Lessons start date has to be between semester's start date and end date")

        if( (data['lessons_end_date'] > data['end_date']) or  (data['lessons_end_date'] < data['start_date']) ):
           errors['lessons_end_date'] = _("Lessons end date has to be between semester's start date and end date")
        
        if data["academic_calendar"].organization.id != data["organization"].id:
            raise serializers.ValidationError(_("You don't have permission to create semesters on this calendar"))
            
        if data["academic_calendar"].deleted_at != None:
            raise serializers.ValidationError(_("Could not find the academic calendar."))
        
        instance_id = None
        if self.instance != None:
            instance_id = self.instance.id
        
        #Verificar se um semestre ta começando ou finalizando no meio de outro
        semesters = Semester.objects.filter(
            academic_calendar = data["academic_calendar"],
            deleted_at__isnull = True, 
            academic_calendar__deleted_at__isnull = True
            ).filter( 
                Q(
                    start_date__lte = data['start_date'], 
                    end_date__gte = data['start_date']
                ) 
                | 
                Q(
                    start_date__lte = data['end_date'],
                    end_date__gte = data['end_date']
                )
            ).exclude(id=instance_id).count()
        
        if semesters > 0:
            raise serializers.ValidationError(_("A semester can't start or end during another semester"))
        
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        
        return data
    
class CalendarSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField(required = False, default = None, min_value=0, max_value = sys.maxsize)
    start_date = serializers.DateField(required = False, default = None)
    end_date = serializers.DateField(required = False, default = None) 
    description = serializers.CharField(required = False, default = None)

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = [
            'id', 
            'name', 
            'organization',
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'organization',
            'email', 
            'first_name',
            'last_name'
        ]

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id', 
            'name', 
            'minutes_per_lesson',
            'min_minutes_per_day'
        ]
        