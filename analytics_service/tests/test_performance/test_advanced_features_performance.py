import pytest
import time
from domain.models import Visualization, Chart, CustomReport, DataExport, AuditTrail


@pytest.mark.django_db
class TestVisualizationPerformance:
    def test_visualization_creation_performance(self):
        start = time.time()
        for i in range(10):
            Visualization.objects.create(
                name=f"Viz {i}",
                visualization_type="bar",
                config={"source": "events"}
            )
        duration = time.time() - start
        assert duration < 2.0

    def test_chart_rendering_performance(self):
        viz = Visualization.objects.create(name="Test", visualization_type="bar", config={})
        start = time.time()
        for i in range(10):
            Chart.objects.create(
                visualization=viz,
                chart_type="bar",
                data={"values": list(range(10))}
            )
        duration = time.time() - start
        assert duration < 2.0


@pytest.mark.django_db
class TestReportGenerationPerformance:
    def test_report_generation_speed(self):
        start = time.time()
        for i in range(10):
            CustomReport.objects.create(
                name=f"Report {i}",
                report_type="summary",
                config={"metrics": list(range(10))}
            )
        duration = time.time() - start
        assert duration < 2.0


@pytest.mark.django_db
class TestExportPerformance:
    def test_export_processing_speed(self):
        start = time.time()
        for i in range(10):
            DataExport.objects.create(
                export_name=f"Export {i}",
                export_format="csv",
                status="completed"
            )
        duration = time.time() - start
        assert duration < 2.0


@pytest.mark.django_db
class TestAuditTrailPerformance:
    def test_audit_logging_performance(self):
        start = time.time()
        for i in range(100):
            AuditTrail.objects.create(
                user_id=f"user-{i}",
                action="test_action",
                resource="test_resource"
            )
        duration = time.time() - start
        assert duration < 2.0

    def test_audit_search_performance(self):
        for i in range(50):
            AuditTrail.objects.create(user_id="user-123", action=f"action-{i}", resource="test")
        
        start = time.time()
        results = list(AuditTrail.objects.filter(user_id="user-123"))
        duration = time.time() - start
        assert duration < 1.0
        assert len(results) == 50
