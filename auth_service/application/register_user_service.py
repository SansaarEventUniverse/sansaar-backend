import re
from pathlib import Path

from django.core.exceptions import ValidationError

from domain.user_model import User


class RegisterUserService:
    def __init__(self):
        self._load_disposable_domains()

    def _load_disposable_domains(self):
        file_path = Path(__file__).parent / 'data' / 'disposable_email_domains.txt'
        with open(file_path) as f:
            self.disposable_domains = {line.strip() for line in f if line.strip()}

    def register(self, data):
        self._validate_terms(data.get('agree_terms'))
        self._validate_passwords(data.get('password'), data.get('confirm_password'))
        self._validate_email(data.get('email'))

        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        return user

    def _validate_terms(self, agree_terms):
        if not agree_terms:
            raise ValidationError('You must agree to the terms and conditions')

    def _validate_passwords(self, password, confirm_password):
        if password != confirm_password:
            raise ValidationError('Passwords do not match')

        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters')

        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')

        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character')

    def _validate_email(self, email):
        domain = email.split('@')[1] if '@' in email else ''
        if domain in self.disposable_domains:
            raise ValidationError('Disposable email addresses are not allowed')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
