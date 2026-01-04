from domain.models import ForumPost

class ModerationService:
    def moderate_post(self, post_id):
        post = ForumPost.objects.get(id=post_id)
        post.moderate()
        return post
