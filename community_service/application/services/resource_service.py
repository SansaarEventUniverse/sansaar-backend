from domain.models import ResourceLibrary, SharedResource

class ResourceSharingService:
    def upload_resource(self, data):
        return SharedResource.objects.create(**data)

    def get_resource(self, resource_id):
        return SharedResource.objects.get(id=resource_id)

    def download_resource(self, resource_id):
        resource = SharedResource.objects.get(id=resource_id)
        resource.increment_download()
        return resource

class LibraryManagementService:
    def create_library(self, data):
        return ResourceLibrary.objects.create(**data)

    def get_library(self, library_id):
        return ResourceLibrary.objects.get(id=library_id)

    def get_all_libraries(self):
        return ResourceLibrary.objects.filter(is_public=True)

    def get_library_resources(self, library_id):
        return SharedResource.objects.filter(library_id=library_id)

class ResourceSearchService:
    def search_by_title(self, query):
        return SharedResource.objects.filter(title__icontains=query)

    def search_by_tags(self, tags):
        return SharedResource.objects.filter(tags__contains=tags)

    def search_by_category(self, category):
        return SharedResource.objects.filter(library__category=category)
