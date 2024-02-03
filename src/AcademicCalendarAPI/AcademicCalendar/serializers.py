from rest_framework import serializers
from .models import *
from django.conf import settings
from django.utils.translation import gettext as _
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
            'academic_calendar'
        ]

    def validate_hexadecimal_color(self, value):
        if re.search(r"([0-9a-fA-F]){6}", value) == None:
            raise serializers.ValidationError(_("Color has to be a number in a hexadecimal format"))
        
        return value
    
    def validate(self, data):
        if(data['end_date'] < data['start_date']):
           raise serializers.ValidationError(_("End date has to be after start date"))
        
        if data["type"] == "RH" and len(data["campi"]) == 0:
            raise serializers.ValidationError(_("A campus must be provided for this regional holiday"))
        
        return data