from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_email_verified", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    def verify_email(self):
        self.is_email_verified = True
        self.save(update_fields=["is_email_verified"])

    def activate(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def has_mfa_enabled(self):
        return hasattr(self, "mfa_secret") and self.mfa_secret.is_verified

    def is_locked_out(self):
        """Check if user is locked out due to failed login attempts"""
        from django.utils import timezone
        from domain.login_attempt_model import LOCKOUT_THRESHOLD, LOCKOUT_DURATION

        cutoff_time = timezone.now() - timezone.timedelta(minutes=LOCKOUT_DURATION)
        recent_failed_attempts = self.login_attempts.filter(success=False, created_at__gte=cutoff_time).count()

        return recent_failed_attempts >= LOCKOUT_THRESHOLD

    def reset_login_attempts(self):
        """Reset all login attempts for user"""
        self.login_attempts.all().delete()

    def has_used_password(self, password):
        """Check if password was used in history"""
        from domain.password_history_model import PASSWORD_HISTORY_SIZE

        recent_passwords = self.password_history.all()[:PASSWORD_HISTORY_SIZE]
        for history in recent_passwords:
            if self.check_password_hash(password, history.password_hash):
                return True
        return False

    def check_password_hash(self, password, password_hash):
        """Check if password matches the given hash"""
        from django.contrib.auth.hashers import check_password

        return check_password(password, password_hash)

    def add_password_to_history(self, password_hash):
        """Add password to history and maintain size limit"""
        from domain.password_history_model import PASSWORD_HISTORY_SIZE, PasswordHistory

        PasswordHistory.objects.create(user=self, password_hash=password_hash)

        # Keep only last N passwords
        old_passwords = self.password_history.all()[PASSWORD_HISTORY_SIZE:]
        for old_password in old_passwords:
            old_password.delete()
