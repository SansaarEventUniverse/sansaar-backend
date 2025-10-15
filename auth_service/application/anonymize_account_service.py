import uuid

from domain.models import AccountDeactivation, User


class AnonymizeAccountService:
    def anonymize(self, user_id: str) -> dict:
        try:
            user = User.objects.get(id=user_id)
            deactivation = AccountDeactivation.objects.get(user_id=str(user.id))

            # Anonymize user data
            anonymous_id = str(uuid.uuid4())[:8]
            user.email = f"deleted_{anonymous_id}@anonymized.local"
            user.username = f"deleted_user_{anonymous_id}"
            user.first_name = "Deleted"
            user.last_name = "User"
            user.is_active = False
            user.save()

            # Mark as anonymized
            deactivation.mark_anonymized()

            return {"message": "Account anonymized successfully", "user_id": str(user.id)}
        except User.DoesNotExist:
            raise ValueError(f"User not found: {user_id}")
        except AccountDeactivation.DoesNotExist:
            raise ValueError(f"No deactivation record found for user: {user_id}")
