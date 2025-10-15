from domain.models import AccountDeactivation, User


class ReactivateAccountService:
    def reactivate(self, user_id: str, is_superadmin: bool = False) -> dict:
        try:
            user = User.objects.get(id=user_id)
            deactivation = AccountDeactivation.objects.get(user_id=str(user.id))

            # Check reactivation permissions
            if not is_superadmin and not deactivation.can_self_reactivate():
                raise ValueError("Grace period expired. Contact administrator to reactivate your account.")

            if is_superadmin and not deactivation.can_superadmin_reactivate():
                raise ValueError("Account is anonymized and cannot be reactivated")

            user.is_active = True
            user.save()

            deactivation.delete()

            return {"message": "Account reactivated successfully", "user_id": str(user.id)}
        except User.DoesNotExist:
            raise ValueError(f"User not found: {user_id}")
        except AccountDeactivation.DoesNotExist:
            raise ValueError(f"No deactivation record found for user: {user_id}")
