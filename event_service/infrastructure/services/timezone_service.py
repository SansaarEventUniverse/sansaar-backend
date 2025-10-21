from typing import List
import pytz


class TimezoneDatabase:
    """Service for timezone database operations."""
    
    def get_all_timezones(self) -> List[str]:
        """Get all available timezones."""
        return pytz.all_timezones
    
    def get_common_timezones(self) -> List[str]:
        """Get common timezones."""
        return pytz.common_timezones
    
    def validate_timezone(self, tz_name: str) -> bool:
        """Validate if timezone exists."""
        return tz_name in pytz.all_timezones
