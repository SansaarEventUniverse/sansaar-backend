from domain.user_profile_model import UserProfile


class ListProfilesService:
    def list_profiles(self, page: int = 1, limit: int = 50):
        offset = (page - 1) * limit
        profiles = UserProfile.objects.all()[offset : offset + limit]
        total = UserProfile.objects.count()
        return {
            "users": [
                {
                    "user_id": p.user_id,
                    "email": p.email,
                    "first_name": p.first_name,
                    "last_name": p.last_name,
                    "bio": p.bio,
                    "profile_picture_url": p.profile_picture_url,
                    "created_at": p.created_at.isoformat(),
                    "updated_at": p.updated_at.isoformat(),
                }
                for p in profiles
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }
