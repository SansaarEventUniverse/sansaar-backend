from domain.models import User


class UserRepository:
    @staticmethod
    def anonymize_user_data(user_id: str, anonymized_email: str) -> User:
        user = User.objects.get(id=user_id)
        user.email = anonymized_email
        user.first_name = "Deleted"
        user.last_name = "User"
        user.is_active = False
        user.save()
        return user

    @staticmethod
    def get_user_by_id(user_id: str) -> User:
        return User.objects.get(id=user_id)

    @staticmethod
    def is_user_anonymized(user_id: str) -> bool:
        user = User.objects.get(id=user_id)
        return (
            user.email.startswith("deleted_")
            and user.email.endswith("@anonymized.local")
            and user.first_name == "Deleted"
            and user.last_name == "User"
            and not user.is_active
        )
