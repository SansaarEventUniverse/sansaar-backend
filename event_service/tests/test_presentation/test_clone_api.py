import uuid
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytz

from domain.event import Event
from domain.clone import EventClone


class CloneEventAPITest(TestCase):
    """Tests for clone event API endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.organizer_id = uuid.uuid4()
        self.event = Event.objects.create(
            title='Original Event',
            description='Test event',
            start_datetime=datetime(2026, 3, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 3, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=self.organizer_id,
        )
    
    def test_clone_event(self):
        """Test cloning an event."""
        url = reverse('clone_event', args=[str(self.event.id)])
        data = {'cloned_by': str(uuid.uuid4())}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['title'], 'Original Event (Copy)')
    
    def test_clone_with_customizations(self):
        """Test cloning with customizations."""
        url = reverse('clone_event', args=[str(self.event.id)])
        data = {
            'cloned_by': str(uuid.uuid4()),
            'customizations': {'title': 'Custom Clone'},
            'reason': 'Testing'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Custom Clone')
    
    def test_clone_invalid_event(self):
        """Test cloning non-existent event."""
        url = reverse('clone_event', args=[str(uuid.uuid4())])
        data = {'cloned_by': str(uuid.uuid4())}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BulkCloneAPITest(TestCase):
    """Tests for bulk clone API endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.organizer_id = uuid.uuid4()
        self.events = [
            Event.objects.create(
                title=f'Event {i}',
                description='Test',
                start_datetime=datetime(2026, 3, i, 10, 0, tzinfo=pytz.UTC),
                end_datetime=datetime(2026, 3, i, 12, 0, tzinfo=pytz.UTC),
                timezone='UTC',
                organizer_id=self.organizer_id,
            )
            for i in range(1, 4)
        ]
    
    def test_bulk_clone(self):
        """Test bulk cloning events."""
        url = reverse('bulk_clone')
        data = {
            'event_ids': [str(e.id) for e in self.events],
            'cloned_by': str(uuid.uuid4())
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)


class CloneSeriesAPITest(TestCase):
    """Tests for clone series API endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.event = Event.objects.create(
            title='Series Event',
            description='Test',
            start_datetime=datetime(2026, 3, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 3, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=uuid.uuid4(),
        )
    
    def test_clone_series(self):
        """Test cloning event as series."""
        url = reverse('clone_series', args=[str(self.event.id)])
        data = {
            'cloned_by': str(uuid.uuid4()),
            'count': 3,
            'interval_days': 7
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)


class GetClonesAPITest(TestCase):
    """Tests for get clones API endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.organizer_id = uuid.uuid4()
        self.original = Event.objects.create(
            title='Original',
            description='Test',
            start_datetime=datetime(2026, 3, 1, 10, 0, tzinfo=pytz.UTC),
            end_datetime=datetime(2026, 3, 1, 12, 0, tzinfo=pytz.UTC),
            timezone='UTC',
            organizer_id=self.organizer_id,
        )
        
        # Create clones
        from application.clone_service import CloneEventService
        service = CloneEventService()
        self.clone1 = service.clone_event(self.original.id, uuid.uuid4())
        self.clone2 = service.clone_event(self.original.id, uuid.uuid4())
    
    def test_get_clones(self):
        """Test getting all clones of an event."""
        url = reverse('get_clones', args=[str(self.original.id)])
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
