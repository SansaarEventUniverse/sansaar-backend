import pytest
from rest_framework.test import APIClient
from domain.models import InterestGroup, Connection, SharedContent, Achievement

@pytest.mark.django_db
class TestSocialNetworkingWorkflow:
    """End-to-end test for complete social networking workflow"""
    
    def test_complete_connection_workflow(self):
        """Test: User sends connection → Accept → Get connections"""
        client = APIClient()
        
        # Step 1: Send connection request
        response = client.post('/api/community/connections/connect/', 
                             {'from_user_id': 1, 'to_user_id': 2}, format='json')
        assert response.status_code == 201
        connection_id = response.data['id']
        
        # Step 2: Accept connection
        response = client.put(f'/api/community/connections/{connection_id}/status/', 
                            {'action': 'accept'}, format='json')
        assert response.status_code == 200
        assert response.data['status'] == 'accepted'
        
        # Step 3: Get user connections
        response = client.get('/api/community/connections/?user_id=1')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        
        # Step 4: Get recommendations
        response = client.get('/api/community/connections/recommendations/?user_id=1')
        assert response.status_code == 200

@pytest.mark.django_db
class TestInterestGroupWorkflow:
    """End-to-end test for interest group workflow"""
    
    def test_complete_group_workflow(self):
        """Test: Create group → Join group → Get members → Get recommendations"""
        client = APIClient()
        
        # Step 1: Create interest group
        response = client.post('/api/community/interest-groups/create/', {
            'name': 'Tech Enthusiasts',
            'description': 'For tech lovers',
            'category': 'technology',
            'creator_user_id': 1
        }, format='json')
        assert response.status_code == 201
        group_id = response.data['id']
        
        # Step 2: Join group
        response = client.post(f'/api/community/interest-groups/{group_id}/join/', 
                             {'user_id': 2}, format='json')
        assert response.status_code == 201
        
        # Step 3: Get groups by category
        response = client.get('/api/community/interest-groups/?category=technology')
        assert response.status_code == 200
        assert len(response.data['results']) >= 1
        
        # Step 4: Get recommendations
        response = client.get('/api/community/interest-groups/recommendations/?user_id=2')
        assert response.status_code == 200

@pytest.mark.django_db
class TestContentCollaborationWorkflow:
    """End-to-end test for content sharing and collaboration"""
    
    def test_complete_content_workflow(self):
        """Test: Share content → Add collaborators → Get collaborators → Get shared content"""
        client = APIClient()
        
        # Step 1: Share content
        response = client.post('/api/community/content/share/', {
            'title': 'My Article',
            'description': 'Great content',
            'content_type': 'article',
            'creator_user_id': 1,
            'status': 'published',
            'is_collaborative': True
        }, format='json')
        assert response.status_code == 201
        content_id = response.data['id']
        
        # Step 2: Add collaborator as editor
        response = client.post(f'/api/community/content/{content_id}/collaborate/', 
                             {'user_id': 2, 'role': 'editor'}, format='json')
        assert response.status_code == 201
        
        # Step 3: Add another collaborator as viewer
        response = client.post(f'/api/community/content/{content_id}/collaborate/', 
                             {'user_id': 3, 'role': 'viewer'}, format='json')
        assert response.status_code == 201
        
        # Step 4: Get all collaborators
        response = client.get(f'/api/community/content/{content_id}/collaborators/')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
        
        # Step 5: Get shared content
        response = client.get('/api/community/content/shared/')
        assert response.status_code == 200
        assert len(response.data['results']) >= 1

@pytest.mark.django_db
class TestAchievementWorkflow:
    """End-to-end test for achievement system"""
    
    def test_complete_achievement_workflow(self):
        """Test: Create achievement → Track progress → Complete → Get user progress"""
        client = APIClient()
        
        # Step 1: Create achievement
        response = client.post('/api/community/achievements/create/', {
            'name': 'First Post',
            'description': 'Create your first post',
            'category': 'participation',
            'points': 10,
            'criteria': 'Create 1 post'
        }, format='json')
        assert response.status_code == 201
        
        # Step 2: Get all achievements
        response = client.get('/api/community/achievements/')
        assert response.status_code == 200
        assert len(response.data['results']) >= 1
        
        # Step 3: Get user achievements
        response = client.get('/api/community/users/1/achievements/')
        assert response.status_code == 200
        
        # Step 4: Get user progress
        response = client.get('/api/community/users/1/progress/')
        assert response.status_code == 200
        assert 'total_achievements' in response.data
