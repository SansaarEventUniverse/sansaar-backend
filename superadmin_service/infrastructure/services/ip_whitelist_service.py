from domain.ip_whitelist_model import IPWhitelist


class IPWhitelistService:
    def is_whitelisted(self, ip_address: str) -> bool:
        return IPWhitelist.objects.filter(ip_address=ip_address, is_active=True).exists()
