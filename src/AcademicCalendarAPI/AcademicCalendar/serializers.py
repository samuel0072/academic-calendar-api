from rest_framework import serializers
from .models import *

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCalendar
        fields = ['id', 'start_date', 'end_date', 'description']

    def validate(self, data):
        errors = {}
            
        if(data['end_date'] < data['start_date']):
            errors['end_date'] = ["A data final tem que ser depois da data inicial"]
            
        if(len(errors) > 0):
            raise serializers.ValidationError(errors)
        
        return data
        