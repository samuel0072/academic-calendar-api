from AcademicCalendar.services.BaseService import BaseService

from AcademicCalendar.serializers import OrganizationSerializer

class OrganizationService(BaseService):

    def getOrgInfo(self):
        org = OrganizationSerializer(self.user.organization)

        return org.data
    
    def updateMinutesInfo(self, data):
        org = OrganizationSerializer(self.user.organization, data={'minutes_per_lesson': data["minutes_per_lesson"], 'min_minutes_per_day': data["min_minutes_per_day"]}, partial=True)

        org.is_valid(raise_exception=True)
        org.save()

        return org.data
