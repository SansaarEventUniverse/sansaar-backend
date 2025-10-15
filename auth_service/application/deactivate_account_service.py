from domain.models import AccountDeactivation, User


class DeactivateAccountService:
    def deactivate(self, user_id: str, reason: str = None) -> dict:
        try:
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()

            deactivation = AccountDeactivation.objects.create(user_id=str(user.id), reason=reason)

            return {
                "message": "Account deactivated successfully",
                "user_id": str(user.id),
                "grace_period_ends": deactivation.grace_period_ends.isoformat(),
                "can_reactivate_until": deactivation.grace_period_ends.isoformat(),
            }
        except User.DoesNotExist:
            raise ValueError(f"User not found: {user_id}")
