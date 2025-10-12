import pytest

from domain.ip_whitelist_model import IPWhitelist
from infrastructure.services.ip_whitelist_service import IPWhitelistService


@pytest.mark.django_db
class TestIPWhitelistService:
    def test_is_whitelisted_true(self):
        IPWhitelist.objects.create(ip_address="192.168.1.1", is_active=True)
        service = IPWhitelistService()
        assert service.is_whitelisted("192.168.1.1") is True

    def test_is_whitelisted_false(self):
        service = IPWhitelistService()
        assert service.is_whitelisted("192.168.1.1") is False

    def test_is_whitelisted_inactive(self):
        IPWhitelist.objects.create(ip_address="192.168.1.1", is_active=False)
        service = IPWhitelistService()
        assert service.is_whitelisted("192.168.1.1") is False
