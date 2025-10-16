from django.urls import path

from .views.account_views import anonymize_account, deactivate_account, delete_account, reactivate_account, verify_anonymization
from .views.auth_views import (
    change_password,
    google_callback,
    login,
    logout,
    register,
    request_password_reset,
    resend_verification,
    reset_password,
    verify_email,
)
from .views.health_views import health_check
from .views.mfa_views import disable_mfa, enable_mfa, verify_mfa
from .views.session_views import list_sessions, revoke_all_sessions, revoke_session

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("verify-email/<str:token>/", verify_email, name="verify_email"),
    path("resend-verification/", resend_verification, name="resend_verification"),
    path("password-reset/request/", request_password_reset, name="request_password_reset"),
    path("password-reset/confirm/", reset_password, name="reset_password"),
    path("password-change/", change_password, name="change_password"),
    path("mfa/enable/", enable_mfa, name="enable_mfa"),
    path("mfa/verify/", verify_mfa, name="verify_mfa"),
    path("mfa/disable/", disable_mfa, name="disable_mfa"),
    path("sessions/", list_sessions, name="list_sessions"),
    path("sessions/<int:session_id>/", revoke_session, name="revoke_session"),
    path("sessions/all/", revoke_all_sessions, name="revoke_all_sessions"),
    path("google/callback/", google_callback, name="google_callback"),
    path("account/<str:user_id>/deactivate/", deactivate_account, name="deactivate_account"),
    path("account/<str:user_id>/reactivate/", reactivate_account, name="reactivate_account"),
    path("account/<str:user_id>/delete/", delete_account, name="delete_account"),
    path("account/<str:user_id>/anonymize/", anonymize_account, name="anonymize_account"),
    path("account/<str:user_id>/verify-anonymization/", verify_anonymization, name="verify_anonymization"),
]
