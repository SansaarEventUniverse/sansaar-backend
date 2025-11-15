from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
import uuid

from domain.ticket_type import TicketType
from infrastructure.services.inventory_cache import TicketInventoryCache
from infrastructure.repositories.ticket_type_repository import TicketTypeRepository


class TicketInventoryCacheTest(TestCase):
    """Tests for TicketInventoryCache."""
    
    def setUp(self):
        self.cache = TicketInventoryCache()
        self.ticket_type_id = uuid.uuid4()
    
    def tearDown(self):
        self.cache.delete_cache(self.ticket_type_id)
    
    def test_set_and_get_available_count(self):
        """Test setting and getting available count."""
        self.cache.set_available_count(self.ticket_type_id, 100)
        count = self.cache.get_available_count(self.ticket_type_id)
        self.assertEqual(count, 100)
    
    def test_decrement_count(self):
        """Test decrementing count."""
        self.cache.set_available_count(self.ticket_type_id, 100)
        new_count = self.cache.decrement_count(self.ticket_type_id, 10)
        self.assertEqual(new_count, 90)
    
    def test_increment_count(self):
        """Test incrementing count."""
        self.cache.set_available_count(self.ticket_type_id, 100)
        new_count = self.cache.increment_count(self.ticket_type_id, 10)
        self.assertEqual(new_count, 110)


class TicketTypeRepositoryTest(TestCase):
    """Tests for TicketTypeRepository."""
    
    def setUp(self):
        self.repository = TicketTypeRepository()
        self.event_id = uuid.uuid4()
        self.now = timezone.now()
        
        # Create test ticket types
        TicketType.objects.create(
            event_id=self.event_id,
            name='VIP',
            price=Decimal('100.00'),
            quantity=50,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=30)
        )
        TicketType.objects.create(
            event_id=self.event_id,
            name='General',
            price=Decimal('50.00'),
            quantity=100,
            sale_start=self.now - timedelta(hours=1),
            sale_end=self.now + timedelta(days=30)
        )
    
    def test_get_by_event(self):
        """Test getting ticket types by event."""
        types = self.repository.get_by_event(self.event_id)
        self.assertEqual(len(types), 2)
        self.assertEqual(types[0].name, 'General')  # Ordered by price
    
    def test_get_available_types(self):
        """Test getting available ticket types."""
        types = self.repository.get_available_types(self.event_id)
        self.assertEqual(len(types), 2)
