import pytest

from domain.ip_whitelist_model import IPWhitelist


@pytest.mark.django_db
class TestIPWhitelistModel:
    def test_create_ip_whitelist(self):
        ip = IPWhitelist.objects.create(ip_address="192.168.1.1", description="Office IP")
        assert ip.ip_address == "192.168.1.1"
        assert ip.description == "Office IP"
        assert ip.is_active is True

    def test_unique_ip_address(self):
        IPWhitelist.objects.create(ip_address="192.168.1.1")
        with pytest.raises(Exception):
            IPWhitelist.objects.create(ip_address="192.168.1.1")

    def test_ipv6_address(self):
        ip = IPWhitelist.objects.create(ip_address="2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        assert ip.ip_address == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
