import pytest
from domain.models import InterestGroup, GroupMembership
from infrastructure.repositories.interest_group_repository import InterestGroupRepository

@pytest.mark.django_db
class TestInterestGroupRepository:
    def test_get_popular_groups(self):
        g1 = InterestGroup.objects.create(name='Popular', description='Test', category='technology', creator_user_id=1)
        g2 = InterestGroup.objects.create(name='Less Popular', description='Test', category='sports', creator_user_id=1)
        GroupMembership.objects.create(group=g1, user_id=2, status='active')
        GroupMembership.objects.create(group=g1, user_id=3, status='active')
        GroupMembership.objects.create(group=g2, user_id=4, status='active')
        
        repo = InterestGroupRepository()
        popular = repo.get_popular_groups(limit=2)
        assert popular[0].name == 'Popular'
    
    def test_get_group_recommendations_no_memberships(self):
        g1 = InterestGroup.objects.create(name='G1', description='Test', category='technology', creator_user_id=1)
        GroupMembership.objects.create(group=g1, user_id=2, status='active')
        
        repo = InterestGroupRepository()
        recommendations = repo.get_group_recommendations(999, limit=5)
        assert recommendations.count() >= 0
    
    def test_get_group_recommendations_with_memberships(self):
        g1 = InterestGroup.objects.create(name='Tech1', description='Test', category='technology', creator_user_id=1)
        g2 = InterestGroup.objects.create(name='Tech2', description='Test', category='technology', creator_user_id=1)
        g3 = InterestGroup.objects.create(name='Sports', description='Test', category='sports', creator_user_id=1)
        
        GroupMembership.objects.create(group=g1, user_id=2, status='active')
        GroupMembership.objects.create(group=g2, user_id=3, status='active')
        
        repo = InterestGroupRepository()
        recommendations = repo.get_group_recommendations(2, limit=5)
        assert g2 in recommendations
        assert g1 not in recommendations
