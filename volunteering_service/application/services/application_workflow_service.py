from domain.models import VolunteerApplication

class ApplicationWorkflowService:
    def approve(self, application_id):
        application = VolunteerApplication.objects.get(id=application_id)
        application.approve()
        return application
    
    def reject(self, application_id):
        application = VolunteerApplication.objects.get(id=application_id)
        application.reject()
        return application
