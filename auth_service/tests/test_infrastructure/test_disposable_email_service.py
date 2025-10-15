import pytest

from infrastructure.services.disposable_email_service import DisposableEmailService


class TestDisposableEmailService:
    def setup_method(self):
        self.service = DisposableEmailService()

    def test_disposable_email_detected(self):
        assert self.service.is_disposable("test@tempmail.com") is True
        assert self.service.is_disposable("user@guerrillamail.com") is True
        assert self.service.is_disposable("test@10minutemail.com") is True

    def test_valid_email_not_disposable(self):
        assert self.service.is_disposable("test@gmail.com") is False
        assert self.service.is_disposable("user@yahoo.com") is False
        assert self.service.is_disposable("admin@company.com") is False

    def test_case_insensitive(self):
        assert self.service.is_disposable("test@TempMail.COM") is True
        assert self.service.is_disposable("TEST@GMAIL.COM") is False

    def test_invalid_email_format(self):
        assert self.service.is_disposable("invalid-email") is False
        assert self.service.is_disposable("") is False
