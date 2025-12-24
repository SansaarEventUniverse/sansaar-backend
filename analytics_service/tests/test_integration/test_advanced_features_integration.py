import pytest
from domain.models import Visualization, Chart, CustomReport, ReportTemplate, DataExport, AuditTrail
from application.services.visualization_service import VisualizationService
from application.services.chart_generation_service import ChartGenerationService
from application.services.report_builder_service import ReportBuilderService
from application.services.data_export_service import DataExportService
from application.services.audit_trail_service import AuditTrailService
from infrastructure.export.export_pipeline import ExportPipeline
from infrastructure.audit.compliance_monitor import ComplianceMonitor


@pytest.mark.django_db
class TestVisualizationIntegration:
    def test_chart_rendering_pipeline(self):
        service = VisualizationService()
        viz = service.create_visualization("Sales Chart", "bar", {"source": "sales"})
        
        chart_service = ChartGenerationService()
        chart = chart_service.generate_chart(viz.id, "bar", {"values": [1, 2, 3]})
        
        assert chart.visualization_id == viz.id
        assert chart.data["values"] == [1, 2, 3]


@pytest.mark.django_db
class TestReportGenerationIntegration:
    def test_report_generation_workflow(self):
        service = ReportBuilderService()
        report = service.build_report("Sales Report", "sales", {"revenue": 1000})
        
        assert report.name == "Sales Report"
        assert report.config["revenue"] == 1000


@pytest.mark.django_db
class TestExportPipelineIntegration:
    def test_export_pipeline_workflow(self):
        service = DataExportService()
        export = service.create_export("Test Export", "csv")
        
        assert export.export_format == "csv"
        assert export.status == "pending"


@pytest.mark.django_db
class TestComplianceMonitoringIntegration:
    def test_compliance_monitoring_workflow(self):
        AuditTrail.objects.create(user_id="user-123", action="data_access", resource="user_data")
        AuditTrail.objects.create(user_id="user-456", action="data_export", resource="reports")
        
        monitor = ComplianceMonitor()
        result = monitor.monitor("gdpr")
        
        assert result["compliant"] is True
        assert result["audit_count"] == 2
        
        report = monitor.generate_report("gdpr")
        assert report.report_type == "gdpr"
        assert report.findings["total_audits"] == 2


@pytest.mark.django_db
class TestAuditTrailIntegration:
    def test_audit_trail_workflow(self):
        service = AuditTrailService()
        
        audit1 = service.log_action("user-123", "login", "auth")
        audit2 = service.log_action("user-123", "view_report", "report-1")
        
        trails = service.get_user_audit_trail("user-123")
        
        assert len(trails) == 2
        assert trails[0].action == "login"
        assert trails[1].action == "view_report"
