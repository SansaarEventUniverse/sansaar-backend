import pytest
from domain.models import InterestGroup, GroupMembership
from application.services.interest_group_service import InterestGroupService, GroupMembershipService, GroupModerationService

@pytest.mark.django_db
class TestInterestGroupService:
    def test_create_group(self):
        service = InterestGroupService()
        group = service.create_group({
            'name': 'Tech Group',
            'description': 'For tech lovers',
            'category': 'technology',
            'creator_user_id': 1
        })
        assert group.name == 'Tech Group'
    
    def test_get_active_groups(self):
        InterestGroup.objects.create(name='Active', description='Test', category='sports', creator_user_id=1, is_active=True)
        InterestGroup.objects.create(name='Inactive', description='Test', category='arts', creator_user_id=1, is_active=False)
        service = InterestGroupService()
        groups = service.get_active_groups()
        assert groups.count() == 1
    
    def test_get_groups_by_category(self):
        InterestGroup.objects.create(name='Tech1', description='Test', category='technology', creator_user_id=1)
        InterestGroup.objects.create(name='Tech2', description='Test', category='technology', creator_user_id=1)
        InterestGroup.objects.create(name='Sports', description='Test', category='sports', creator_user_id=1)
        service = InterestGroupService()
        groups = service.get_groups_by_category('technology')
        assert groups.count() == 2

@pytest.mark.django_db
class TestGroupMembershipService:
    def test_join_group(self):
        group = InterestGroup.objects.create(name='Test', description='Test', category='education', creator_user_id=1)
        service = GroupMembershipService()
        membership = service.join_group(group.id, 2)
        assert membership.user_id == 2
        assert membership.status == 'pending'
    
    def test_join_full_group(self):
        group = InterestGroup.objects.create(name='Full', description='Test', category='business', creator_user_id=1, max_members=1)
        GroupMembership.objects.create(group=group, user_id=2, status='active')
        service = GroupMembershipService()
        with pytest.raises(ValueError):
            service.join_group(group.id, 3)
    
    def test_approve_membership(self):
        group = InterestGroup.objects.create(name='Test', description='Test', category='other', creator_user_id=1)
        membership = GroupMembership.objects.create(group=group, user_id=2)
        service = GroupMembershipService()
        updated = service.approve_membership(membership.id)
        assert updated.is_active()
    
    def test_get_user_groups(self):
        group1 = InterestGroup.objects.create(name='G1', description='Test', category='technology', creator_user_id=1)
        group2 = InterestGroup.objects.create(name='G2', description='Test', category='sports', creator_user_id=1)
        GroupMembership.objects.create(group=group1, user_id=2, status='active')
        GroupMembership.objects.create(group=group2, user_id=2, status='active')
        GroupMembership.objects.create(group=group1, user_id=3, status='active')
        service = GroupMembershipService()
        memberships = service.get_user_groups(2)
        assert memberships.count() == 2

@pytest.mark.django_db
class TestGroupModerationService:
    def test_remove_member(self):
        group = InterestGroup.objects.create(name='Test', description='Test', category='arts', creator_user_id=1)
        membership = GroupMembership.objects.create(group=group, user_id=2, status='active')
        service = GroupModerationService()
        updated = service.remove_member(membership.id)
        assert updated.status == 'removed'
    
    def test_promote_member(self):
        group = InterestGroup.objects.create(name='Test', description='Test', category='education', creator_user_id=1)
        membership = GroupMembership.objects.create(group=group, user_id=2, status='active')
        service = GroupModerationService()
        updated = service.promote_member(membership.id)
        assert updated.role == 'moderator'
