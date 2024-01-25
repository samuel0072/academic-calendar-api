from rest_framework import serializers
from .models import *
from django.conf import settings

import re

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalendar
        fields = ['id', 'start_date', 'end_date', 'description', 'organization']

    def validate(self, data):
        errors = {}
            
        if(data['end_date'] < data['start_date']):
            errors['end_date'] = ["A data final tem que ser depois da data inicial"]
            
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
            raise serializers.ValidationError(settings.TRANSLATIONS.ErrorHexadecimalColor.Format)
        
        return value
    
    def validate(self, data):
        print(data['end_date'], data['start_date'])
        if(data['end_date'] < data['start_date']):
           raise serializers.ValidationError("A data final tem que ser depois da data inicial")
        
        return data

# data = {'start_date': "2024-1-1",  'end_date': "2024-12-31",  'description': "evento1",  'organization': 1,  'label': "NSD",  'hexadecimal_color': "FFFFFF",  'academic_calendar':1}