import pytest
from decimal import Decimal
from domain.models import FinancialReport, RevenueAnalytics
from application.services.financial_reporting_service import FinancialReportingService
from application.services.revenue_analytics_service import RevenueAnalyticsService
from application.services.profit_loss_service import ProfitLossService


@pytest.mark.django_db
class TestFinancialReportingService:
    def test_create_financial_report(self):
        service = FinancialReportingService()
        report = service.create_report("event-123", Decimal("10000.00"), Decimal("3000.00"))
        assert report.net_profit == Decimal("7000.00")

    def test_get_financial_report(self):
        FinancialReport.objects.create(event_id="event-123", total_revenue=Decimal("10000.00"))
        service = FinancialReportingService()
        report = service.get_report("event-123")
        assert report.event_id == "event-123"


@pytest.mark.django_db
class TestRevenueAnalyticsService:
    def test_track_ticket_revenue(self):
        service = RevenueAnalyticsService()
        analytics = service.track_ticket_revenue("event-123", Decimal("5000.00"))
        assert analytics.ticket_revenue == Decimal("5000.00")

    def test_track_sponsorship_revenue(self):
        service = RevenueAnalyticsService()
        analytics = service.track_sponsorship_revenue("event-123", Decimal("2000.00"))
        assert analytics.sponsorship_revenue == Decimal("2000.00")


@pytest.mark.django_db
class TestProfitLossService:
    def test_calculate_profit_loss(self):
        FinancialReport.objects.create(
            event_id="event-123",
            total_revenue=Decimal("10000.00"),
            total_expenses=Decimal("3000.00")
        )
        service = ProfitLossService()
        result = service.calculate_profit_loss("event-123")
        assert result['net_profit'] == Decimal("7000.00")
        assert result['profit_margin'] == 70.0
