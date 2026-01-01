from domain.models import VolunteerApplication

class ApplicationRepository:
    def get_pending_applications(self):
        return VolunteerApplication.objects.filter(status='pending')
    
    def get_by_status(self, status):
        return VolunteerApplication.objects.filter(status=status)
    
    def get_by_volunteer_email(self, email):
        return VolunteerApplication.objects.filter(volunteer_email=email)
