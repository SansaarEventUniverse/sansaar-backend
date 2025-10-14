import pytest

from domain.models import IPWhitelist, SuperAdmin


@pytest.mark.django_db
def test_ip_whitelist_security():
    # Whitelist IP
    whitelist = IPWhitelist.objects.create(ip_address="127.0.0.1", is_active=True)

    assert whitelist.is_active
    assert IPWhitelist.objects.filter(is_active=True).count() == 1


@pytest.mark.django_db
def test_mfa_secret_generation():
    admin = SuperAdmin.objects.create(email="admin@test.com", is_active=True)
    secret = admin.generate_mfa_secret()

    assert secret is not None
    assert len(secret) > 0
    assert admin.mfa_secret == secret


@pytest.mark.django_db
def test_password_security():
    admin = SuperAdmin.objects.create(email="admin@test.com", password_hash="hashed_password", is_active=True)

    assert admin.password_hash == "hashed_password"


@pytest.mark.django_db
def test_inactive_admin_validation():
    admin = SuperAdmin.objects.create(email="admin@test.com", is_active=False)
    assert not admin.is_active


@pytest.mark.django_db
def test_mfa_uri_generation():
    admin = SuperAdmin.objects.create(email="admin@test.com", is_active=True)
    admin.generate_mfa_secret()

    uri = admin.get_mfa_uri()
    assert "otpauth://totp/" in uri
    assert "admin" in uri
