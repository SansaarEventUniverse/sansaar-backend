import pytest
from domain.models import InterestGroup, GroupMembership

@pytest.mark.django_db
class TestInterestGroup:
    def test_create_interest_group(self):
        group = InterestGroup.objects.create(
            name='Tech Enthusiasts',
            description='Group for tech lovers',
            category='technology',
            creator_user_id=1
        )
        assert group.name == 'Tech Enthusiasts'
        assert group.is_active is True
    
    def test_group_is_full(self):
        group = InterestGroup.objects.create(
            name='Small Group',
            description='Limited members',
            category='sports',
            creator_user_id=1,
            max_members=2
        )
        GroupMembership.objects.create(group=group, user_id=2, status='active')
        GroupMembership.objects.create(group=group, user_id=3, status='active')
        assert group.is_full() is True
    
    def test_group_not_full_unlimited(self):
        group = InterestGroup.objects.create(
            name='Big Group',
            description='Unlimited',
            category='arts',
            creator_user_id=1,
            max_members=0
        )
        assert group.is_full() is False
    
    def test_deactivate_group(self):
        group = InterestGroup.objects.create(
            name='Test Group',
            description='Test',
            category='education',
            creator_user_id=1
        )
        group.deactivate()
        assert group.is_active is False

@pytest.mark.django_db
class TestGroupMembership:
    def test_create_membership(self):
        group = InterestGroup.objects.create(
            name='Test Group',
            description='Test',
            category='business',
            creator_user_id=1
        )
        membership = GroupMembership.objects.create(group=group, user_id=2)
        assert membership.status == 'pending'
        assert membership.role == 'member'
    
    def test_activate_membership(self):
        group = InterestGroup.objects.create(
            name='Test Group',
            description='Test',
            category='other',
            creator_user_id=1
        )
        membership = GroupMembership.objects.create(group=group, user_id=2)
        membership.activate()
        assert membership.is_active() is True
    
    def test_remove_membership(self):
        group = InterestGroup.objects.create(
            name='Test Group',
            description='Test',
            category='technology',
            creator_user_id=1
        )
        membership = GroupMembership.objects.create(group=group, user_id=2, status='active')
        membership.remove()
        assert membership.status == 'removed'
    
    def test_promote_to_moderator(self):
        group = InterestGroup.objects.create(
            name='Test Group',
            description='Test',
            category='sports',
            creator_user_id=1
        )
        membership = GroupMembership.objects.create(group=group, user_id=2, status='active')
        membership.promote_to_moderator()
        assert membership.role == 'moderator'
