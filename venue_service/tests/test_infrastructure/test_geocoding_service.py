import uuid
from django.test import TestCase
from unittest.mock import patch, MagicMock

from infrastructure.services.geocoding_service import GeocodingService


class GeocodingServiceTest(TestCase):
    """Tests for GeocodingService."""
    
    @patch('infrastructure.services.geocoding_service.googlemaps.Client')
    def test_geocode_address(self, mock_client):
        """Test geocoding an address."""
        mock_instance = MagicMock()
        mock_instance.geocode.return_value = [{
            'geometry': {
                'location': {'lat': 40.7128, 'lng': -74.0060}
            }
        }]
        mock_client.return_value = mock_instance
        
        service = GeocodingService()
        result = service.geocode_address('New York, NY')
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 40.7128)
        self.assertEqual(result[1], -74.0060)
