from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from infrastructure.services.jwt_service import JWTService


class GoogleOAuthAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Handle user before social login"""
        if sociallogin.is_existing:
            return

        # Auto-verify email for OAuth users
        if sociallogin.account.provider == 'google':
            user = sociallogin.user
            user.is_email_verified = True

    def save_user(self, request, sociallogin, form=None):
        """Save OAuth user with verified email"""
        user = super().save_user(request, sociallogin, form)
        user.is_email_verified = True
        user.save()
        return user

    def generate_tokens(self, user):
        """Generate JWT tokens for OAuth user"""
        jwt_service = JWTService()
        return {
            'access_token': jwt_service.generate_access_token(user),
            'refresh_token': jwt_service.generate_refresh_token(user)
        }
