import pytest
import time
from rest_framework.test import APIClient
from domain.models import Connection, InterestGroup, SharedContent, Achievement

@pytest.mark.django_db
class TestPerformance:
    """Performance tests for critical operations"""
    
    def test_connection_query_performance(self):
        """Test connection queries complete within acceptable time"""
        # Create test data
        for i in range(50):
            Connection.objects.create(from_user_id=1, to_user_id=i+2, status='accepted')
        
        client = APIClient()
        start_time = time.time()
        response = client.get('/api/community/connections/?user_id=1')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should complete in less than 1 second
    
    def test_interest_group_listing_performance(self):
        """Test group listing performance with many groups"""
        # Create test data
        for i in range(100):
            InterestGroup.objects.create(
                name=f'Group {i}',
                description='Test',
                category='technology',
                creator_user_id=1
            )
        
        client = APIClient()
        start_time = time.time()
        response = client.get('/api/community/interest-groups/')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Should complete in less than 2 seconds
    
    def test_content_collaboration_performance(self):
        """Test content with many collaborators"""
        content = SharedContent.objects.create(
            title='Test',
            description='Test',
            content_type='article',
            creator_user_id=1,
            status='published'
        )
        
        # Add many collaborators
        client = APIClient()
        start_time = time.time()
        for i in range(20):
            client.post(f'/api/community/content/{content.id}/collaborate/', 
                       {'user_id': i+2, 'role': 'viewer'}, format='json')
        end_time = time.time()
        
        assert (end_time - start_time) < 5.0  # Should complete in less than 5 seconds
    
    def test_achievement_stats_performance(self):
        """Test achievement statistics calculation"""
        # Create achievements
        for i in range(20):
            Achievement.objects.create(
                name=f'Achievement {i}',
                description='Test',
                category='participation',
                points=10,
                criteria='Test'
            )
        
        client = APIClient()
        start_time = time.time()
        response = client.get('/api/community/users/1/progress/')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.5  # Should be very fast
    
    def test_recommendation_algorithm_performance(self):
        """Test recommendation algorithms complete quickly"""
        # Create network
        for i in range(10):
            Connection.objects.create(from_user_id=1, to_user_id=i+2, status='accepted')
            for j in range(5):
                Connection.objects.create(from_user_id=i+2, to_user_id=j+20, status='accepted')
        
        client = APIClient()
        start_time = time.time()
        response = client.get('/api/community/connections/recommendations/?user_id=1')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Recommendation should be fast
