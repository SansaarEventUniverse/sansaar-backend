from django.test import TestCase

from infrastructure.services.timezone_service import TimezoneDatabase


class TimezoneDatabaseTest(TestCase):
    """Tests for TimezoneDatabase."""
    
    def setUp(self):
        self.service = TimezoneDatabase()
        
    def test_get_all_timezones(self):
        """Test getting all timezones."""
        timezones = self.service.get_all_timezones()
        self.assertGreater(len(timezones), 0)
        self.assertIn('UTC', timezones)
        
    def test_get_common_timezones(self):
        """Test getting common timezones."""
        timezones = self.service.get_common_timezones()
        self.assertGreater(len(timezones), 0)
        self.assertIn('America/New_York', timezones)
        
    def test_validate_timezone(self):
        """Test timezone validation."""
        self.assertTrue(self.service.validate_timezone('UTC'))
        self.assertTrue(self.service.validate_timezone('America/New_York'))
        self.assertFalse(self.service.validate_timezone('Invalid/Timezone'))
