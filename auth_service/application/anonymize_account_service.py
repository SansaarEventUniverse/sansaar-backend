import uuid

from application.log_audit_event_service import LogAuditEventService
from domain.audit_log_model import AuditEventType
from domain.models import AccountDeactivation, User
from infrastructure.services.event_publisher import EventPublisher


class AnonymizeUserDataService:
    def __init__(self):
        self.event_publisher = EventPublisher()
        self.audit_service = LogAuditEventService()

    def anonymize(self, user_id: str) -> dict:
        user = User.objects.get(id=user_id)
        deactivation = AccountDeactivation.objects.get(user_id=str(user.id))

        if not deactivation.is_permanently_deactivated:
            raise ValueError("User must be permanently deactivated before anonymization")

        if deactivation.is_anonymized:
            raise ValueError("User data is already anonymized")

        # Generate anonymized values
        anonymous_id = str(uuid.uuid4())[:8]
        anonymized_email = f"deleted_{anonymous_id}@anonymized.local"

        # Store original email for event and audit
        original_email = user.email

        # Anonymize user data
        user.email = anonymized_email
        user.first_name = "Deleted"
        user.last_name = "User"
        user.is_active = False
        user.save()

        # Mark as anonymized
        deactivation.mark_anonymized()

        # Log audit event (preserves user_id reference)
        self.audit_service.log_event(
            event_type=AuditEventType.ACCOUNT_ANONYMIZED,
            user_id=str(user.id),
            success=True,
            metadata={"original_email": original_email, "anonymized_email": anonymized_email},
        )

        # Publish event to user_org_service
        self._publish_anonymization_event(str(user.id), original_email)

        return {
            "message": "Account anonymized successfully",
            "user_id": str(user.id),
            "anonymized_email": anonymized_email,
        }

    def _publish_anonymization_event(self, user_id: str, original_email: str):
        event_data = {"user_id": user_id, "original_email": original_email, "event": "account_anonymized"}
        self.event_publisher.publish_account_anonymized(event_data)

    def verify_anonymization(self, user_id: str) -> dict:
        user = User.objects.get(id=user_id)
        deactivation = AccountDeactivation.objects.get(user_id=str(user.id))

        is_anonymized = (
            deactivation.is_anonymized
            and user.email.startswith("deleted_")
            and user.email.endswith("@anonymized.local")
            and user.first_name == "Deleted"
            and user.last_name == "User"
            and not user.is_active
        )

        return {"user_id": user_id, "is_anonymized": is_anonymized, "anonymized_at": deactivation.anonymized_at}
