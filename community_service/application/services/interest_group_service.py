from domain.models import InterestGroup, GroupMembership

class InterestGroupService:
    def create_group(self, data):
        return InterestGroup.objects.create(**data)
    
    def get_active_groups(self):
        return InterestGroup.objects.filter(is_active=True)
    
    def get_groups_by_category(self, category):
        return InterestGroup.objects.filter(category=category, is_active=True)

class GroupMembershipService:
    def join_group(self, group_id, user_id):
        group = InterestGroup.objects.get(id=group_id)
        if group.is_full():
            raise ValueError('Group is full')
        return GroupMembership.objects.create(group=group, user_id=user_id)
    
    def approve_membership(self, membership_id):
        membership = GroupMembership.objects.get(id=membership_id)
        membership.activate()
        return membership
    
    def get_user_groups(self, user_id):
        return GroupMembership.objects.filter(user_id=user_id, status='active')

class GroupModerationService:
    def remove_member(self, membership_id):
        membership = GroupMembership.objects.get(id=membership_id)
        membership.remove()
        return membership
    
    def promote_member(self, membership_id):
        membership = GroupMembership.objects.get(id=membership_id)
        membership.promote_to_moderator()
        return membership
