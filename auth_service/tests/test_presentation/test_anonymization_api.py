import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from domain.models import AccountDeactivation, AuditLog, User


@pytest.mark.django_db
class TestAnonymizationAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="TestPass123!", first_name="John", last_name="Doe"
        )
        self.user.is_active = False
        self.user.save()

    def test_anonymize_account_success(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        url = reverse("anonymize_account", kwargs={"user_id": str(self.user.id)})
        response = self.client.post(url)

        assert response.status_code == 200
        assert response.data["message"] == "Account anonymized successfully"
        assert "anonymized_email" in response.data

        self.user.refresh_from_db()
        assert self.user.email.startswith("deleted_")
        assert self.user.first_name == "Deleted"

    def test_anonymize_account_not_permanently_deactivated(self):
        AccountDeactivation.objects.create(user_id=str(self.user.id))

        url = reverse("anonymize_account", kwargs={"user_id": str(self.user.id)})
        response = self.client.post(url)

        assert response.status_code == 400
        assert "error" in response.data

    def test_anonymize_account_user_not_found(self):
        url = reverse("anonymize_account", kwargs={"user_id": "999999"})
        response = self.client.post(url)

        assert response.status_code == 404
        assert "error" in response.data

    def test_verify_anonymization_success(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        anonymize_url = reverse("anonymize_account", kwargs={"user_id": str(self.user.id)})
        self.client.post(anonymize_url)

        verify_url = reverse("verify_anonymization", kwargs={"user_id": str(self.user.id)})
        response = self.client.get(verify_url)

        assert response.status_code == 200
        assert response.data["is_anonymized"] is True
        assert response.data["anonymized_at"] is not None

    def test_verify_anonymization_not_anonymized(self):
        AccountDeactivation.objects.create(user_id=str(self.user.id))

        url = reverse("verify_anonymization", kwargs={"user_id": str(self.user.id)})
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.data["is_anonymized"] is False
        assert response.data["anonymized_at"] is None

    def test_anonymization_creates_audit_log(self):
        deactivation = AccountDeactivation.objects.create(user_id=str(self.user.id))
        deactivation.mark_permanently_deactivated()

        url = reverse("anonymize_account", kwargs={"user_id": str(self.user.id)})
        response = self.client.post(url)

        assert response.status_code == 200

        audit_logs = AuditLog.objects.filter(user_id=str(self.user.id), event_type="ACCOUNT_ANONYMIZED")
        assert audit_logs.exists()
        assert audit_logs.first().metadata["original_email"] == "test@example.com"
