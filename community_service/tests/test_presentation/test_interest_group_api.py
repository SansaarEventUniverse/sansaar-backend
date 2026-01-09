import pytest
from rest_framework.test import APIClient
from domain.models import InterestGroup, GroupMembership

@pytest.mark.django_db
class TestInterestGroupAPI:
    def test_create_group(self):
        client = APIClient()
        data = {
            'name': 'Tech Enthusiasts',
            'description': 'For tech lovers',
            'category': 'technology',
            'creator_user_id': 1
        }
        response = client.post('/api/community/interest-groups/create/', data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == 'Tech Enthusiasts'
    
    def test_get_groups(self):
        InterestGroup.objects.create(name='G1', description='Test', category='sports', creator_user_id=1)
        InterestGroup.objects.create(name='G2', description='Test', category='arts', creator_user_id=1)
        client = APIClient()
        response = client.get('/api/community/interest-groups/')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
    
    def test_get_groups_by_category(self):
        InterestGroup.objects.create(name='Tech1', description='Test', category='technology', creator_user_id=1)
        InterestGroup.objects.create(name='Tech2', description='Test', category='technology', creator_user_id=1)
        InterestGroup.objects.create(name='Sports', description='Test', category='sports', creator_user_id=1)
        client = APIClient()
        response = client.get('/api/community/interest-groups/?category=technology')
        assert response.status_code == 200
        assert len(response.data['results']) == 2
    
    def test_join_group(self):
        group = InterestGroup.objects.create(name='Test', description='Test', category='education', creator_user_id=1)
        client = APIClient()
        response = client.post(f'/api/community/interest-groups/{group.id}/join/', {'user_id': 2}, format='json')
        assert response.status_code == 201
        assert response.data['user_id'] == 2
        assert response.data['status'] == 'pending'
    
    def test_join_full_group(self):
        group = InterestGroup.objects.create(name='Full', description='Test', category='business', creator_user_id=1, max_members=1)
        GroupMembership.objects.create(group=group, user_id=2, status='active')
        client = APIClient()
        response = client.post(f'/api/community/interest-groups/{group.id}/join/', {'user_id': 3}, format='json')
        assert response.status_code == 400
    
    def test_get_recommendations(self):
        g1 = InterestGroup.objects.create(name='Tech1', description='Test', category='technology', creator_user_id=1)
        g2 = InterestGroup.objects.create(name='Tech2', description='Test', category='technology', creator_user_id=1)
        GroupMembership.objects.create(group=g1, user_id=2, status='active')
        client = APIClient()
        response = client.get('/api/community/interest-groups/recommendations/?user_id=2')
        assert response.status_code == 200
        assert 'recommendations' in response.data
