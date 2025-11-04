import json
from django.test import TestCase, Client

from domain.category import Category, Tag


class CategoryAPITest(TestCase):
    """Tests for Category API endpoints."""
    
    def setUp(self):
        self.client = Client()
        
    def test_get_categories(self):
        """Test getting categories via API."""
        Category.objects.create(name='Technology', slug='technology')
        Category.objects.create(name='Music', slug='music')
        
        response = self.client.get('/api/events/categories/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('categories', data)
        self.assertEqual(len(data['categories']), 2)
        
    def test_create_category(self):
        """Test creating category via API."""
        data = {
            'name': 'Technology',
            'description': 'Tech events',
        }
        response = self.client.post(
            '/api/events/categories/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Technology')
        
    def test_get_category_stats(self):
        """Test getting category stats via API."""
        Category.objects.create(name='Technology', slug='technology', event_count=10)
        
        response = self.client.get('/api/events/categories/stats/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_categories', data)
        self.assertEqual(data['total_categories'], 1)


class TagAPITest(TestCase):
    """Tests for Tag API endpoints."""
    
    def setUp(self):
        self.client = Client()
        
    def test_get_tags(self):
        """Test getting tags via API."""
        Tag.objects.create(name='python', slug='python', usage_count=100)
        Tag.objects.create(name='django', slug='django', usage_count=50)
        
        response = self.client.get('/api/events/tags/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('tags', data)
        self.assertEqual(len(data['tags']), 2)
        
    def test_create_tag(self):
        """Test creating tag via API."""
        data = {'name': 'python'}
        response = self.client.post(
            '/api/events/tags/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'python')
        
    def test_get_tag_suggestions(self):
        """Test getting tag suggestions via API."""
        Tag.objects.create(name='python', slug='python')
        Tag.objects.create(name='pytorch', slug='pytorch')
        
        response = self.client.get('/api/events/tags/suggestions/?q=py')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)
        self.assertEqual(len(data['suggestions']), 2)
        
    def test_get_tag_stats(self):
        """Test getting tag stats via API."""
        Tag.objects.create(name='python', slug='python', usage_count=100)
        
        response = self.client.get('/api/events/tags/stats/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('total_tags', data)
        self.assertEqual(data['total_tags'], 1)
