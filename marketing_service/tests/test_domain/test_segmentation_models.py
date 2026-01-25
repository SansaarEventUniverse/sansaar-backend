import pytest
from domain.models import AudienceSegment, SegmentRule

@pytest.mark.django_db
class TestAudienceSegment:
    def test_create_segment(self):
        """Test creating audience segment"""
        segment = AudienceSegment.objects.create(
            name="Active Users",
            description="Users active in last 30 days",
            status="active"
        )
        assert segment.name == "Active Users"
        assert segment.status == "active"

    def test_segment_status_choices(self):
        """Test segment status validation"""
        segment = AudienceSegment.objects.create(
            name="Test",
            description="Test segment",
            status="draft"
        )
        assert segment.status in ['draft', 'active', 'archived']

    def test_activate_segment(self):
        """Test activating segment"""
        segment = AudienceSegment.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        segment.activate()
        assert segment.status == "active"

    def test_archive_segment(self):
        """Test archiving segment"""
        segment = AudienceSegment.objects.create(
            name="Test",
            description="Test",
            status="active"
        )
        segment.archive()
        assert segment.status == "archived"

@pytest.mark.django_db
class TestSegmentRule:
    def test_create_rule(self):
        """Test creating segment rule"""
        segment = AudienceSegment.objects.create(
            name="Test Segment",
            description="Test",
            status="draft"
        )
        rule = SegmentRule.objects.create(
            segment=segment,
            field="age",
            operator="greater_than",
            value="18"
        )
        assert rule.field == "age"
        assert rule.operator == "greater_than"

    def test_rule_validation(self):
        """Test rule validation"""
        segment = AudienceSegment.objects.create(
            name="Test",
            description="Test",
            status="draft"
        )
        rule = SegmentRule.objects.create(
            segment=segment,
            field="status",
            operator="equals",
            value="active"
        )
        assert rule.is_valid()
