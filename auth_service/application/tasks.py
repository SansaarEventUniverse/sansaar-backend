from celery import shared_task


@shared_task
def delete_unverified_user(user_id):
    from domain.user_model import User

    try:
        user = User.objects.get(id=user_id)
        if not user.is_email_verified:
            user.delete()
    except User.DoesNotExist:
        pass
