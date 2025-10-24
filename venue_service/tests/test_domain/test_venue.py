import uuid
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal

from domain.venue import Venue


class VenueModelTest(TestCase):
    """Tests for Venue domain model."""
    
    def setUp(self):
        self.owner_id = uuid.uuid4()
        
    def test_create_venue(self):
        """Test creating a valid venue."""
        venue = Venue.objects.create(
            name="Test Venue",
            description="Test Description",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=100,
            owner_id=self.owner_id,
        )
        self.assertIsNotNone(venue.id)
        self.assertEqual(venue.name, "Test Venue")
        self.assertFalse(venue.is_verified)
        
    def test_capacity_validation(self):
        """Test capacity must be positive."""
        venue = Venue(
            name="Test Venue",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=-1,
            owner_id=self.owner_id,
        )
        with self.assertRaises(ValidationError) as cm:
            venue.clean()
        self.assertIn('capacity', cm.exception.message_dict)
        
    def test_latitude_validation(self):
        """Test latitude range validation."""
        venue = Venue(
            name="Test Venue",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=100,
            latitude=Decimal('91.0'),
            owner_id=self.owner_id,
        )
        with self.assertRaises(ValidationError) as cm:
            venue.clean()
        self.assertIn('latitude', cm.exception.message_dict)
        
    def test_longitude_validation(self):
        """Test longitude range validation."""
        venue = Venue(
            name="Test Venue",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=100,
            longitude=Decimal('181.0'),
            owner_id=self.owner_id,
        )
        with self.assertRaises(ValidationError) as cm:
            venue.clean()
        self.assertIn('longitude', cm.exception.message_dict)
        
    def test_verify_venue(self):
        """Test venue verification."""
        venue = Venue.objects.create(
            name="Test Venue",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=100,
            owner_id=self.owner_id,
        )
        venue.verify()
        self.assertTrue(venue.is_verified)
        self.assertIsNotNone(venue.verified_at)
        
    def test_unverify_venue(self):
        """Test removing verification."""
        venue = Venue.objects.create(
            name="Test Venue",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=100,
            owner_id=self.owner_id,
        )
        venue.verify()
        venue.unverify()
        self.assertFalse(venue.is_verified)
        self.assertIsNone(venue.verified_at)
        
    def test_has_coordinates(self):
        """Test coordinate check."""
        venue = Venue.objects.create(
            name="Test Venue",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=100,
            latitude=Decimal('40.7128'),
            longitude=Decimal('-74.0060'),
            owner_id=self.owner_id,
        )
        self.assertTrue(venue.has_coordinates())
        
    def test_soft_delete(self):
        """Test soft delete."""
        venue = Venue.objects.create(
            name="Test Venue",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            capacity=100,
            owner_id=self.owner_id,
        )
        venue.soft_delete()
        self.assertIsNotNone(venue.deleted_at)
