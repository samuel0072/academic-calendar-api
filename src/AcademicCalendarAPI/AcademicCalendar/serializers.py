from rest_framework import serializers
from .models import *
from django.utils.translation import gettext as _
from django.db.models import Q
import re

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
        if re.search(r"([0-9a-fA-F]){6}", value) == None:
            raise serializers.ValidationError(_("Color has to be a number in a hexadecimal format"))
        
        return value
    
    def validate(self, data):
        if(data['end_date'] < data['start_date']):
           raise serializers.ValidationError(_("End date has to be after start date"))
        
        if data["label"] != Event.HOLIDAY and len(data["campi"]) == 0:
            raise serializers.ValidationError(_("A campus must be provided for this event"))
        
        if data["academic_calendar"] != None:
            if data["academic_calendar"].organization.id != data["organization"].id:
                raise serializers.ValidationError(_("You don't have permission to create events on this calendar"))
        
        for campus in data["campi"]:
            if campus.organization.id != data["organization"].id:
                raise serializers.ValidationError(_("You don't have permission to create events on this campus: %(name)s" % {"name": campus.name} ))
        
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
            'academic_calendar'
        ]

    def validate(self, data):
        if(data['end_date'] < data['start_date']):
           raise serializers.ValidationError(_("End date has to be after start date"))
        
        if data["academic_calendar"].organization.id != data["organization"].id:
            raise serializers.ValidationError(_("You don't have permission to create semesters on this calendar"))
        
        #Verificar se um semestre ta começando ou finalizando no meio de outro
        semesters = Semester.objects.filter(academic_calendar = data["academic_calendar"]).filter( 
                Q(
                    start_date__lte = data['start_date'], 
                    end_date__gte = data['start_date']
                ) 
                | 
                Q(
                    start_date__lte = data['end_date'],
                    end_date__gte = data['end_date']
                )
            ).count()
        
        if semesters > 0:
            raise serializers.ValidationError(_("A semester can't start or end during another semester"))
        
        return data
    