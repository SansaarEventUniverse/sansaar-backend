from domain.models import ForumPost, Forum

class PostManagementService:
    def create(self, data):
        forum_id = data.pop('forum_id')
        forum = Forum.objects.get(id=forum_id)
        return ForumPost.objects.create(forum=forum, **data)
    
    def publish(self, post_id):
        post = ForumPost.objects.get(id=post_id)
        post.status = 'published'
        post.save()
        return post
