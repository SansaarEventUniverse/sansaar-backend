from domain.models import AccountDeactivation, User


class DeleteAccountService:
    def delete(self, user_id: str) -> dict:
        try:
            user = User.objects.get(id=user_id)

            # Delete deactivation record if exists
            AccountDeactivation.objects.filter(user_id=str(user.id)).delete()

            # Delete user
            user.delete()

            return {"message": "Account permanently deleted", "user_id": str(user_id)}
        except User.DoesNotExist:
            raise ValueError(f"User not found: {user_id}")
