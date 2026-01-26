from domain.models import ABTest, TestVariant

class ABTestingService:
    def create_test(self, data):
        return ABTest.objects.create(**data)

    def get_tests(self):
        return ABTest.objects.all()

    def get_test(self, test_id):
        return ABTest.objects.get(id=test_id)

class VariantManagementService:
    def create_variant(self, test_id, data):
        test = ABTest.objects.get(id=test_id)
        return TestVariant.objects.create(ab_test=test, **data)

    def get_variants(self, test_id):
        return TestVariant.objects.filter(ab_test_id=test_id)

class TestAnalysisService:
    def analyze_test(self, test_id):
        test = ABTest.objects.get(id=test_id)
        return {'test_id': test_id, 'status': test.status}
