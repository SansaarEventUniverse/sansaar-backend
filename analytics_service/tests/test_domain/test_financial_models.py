import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from domain.models import FinancialReport, RevenueAnalytics


@pytest.mark.django_db
class TestFinancialReport:
    def test_create_financial_report(self):
        report = FinancialReport.objects.create(
            event_id="event-123",
            total_revenue=Decimal("10000.00"),
            total_expenses=Decimal("3000.00")
        )
        assert report.event_id == "event-123"
        assert report.total_revenue == Decimal("10000.00")
        assert report.net_profit == Decimal("7000.00")

    def test_calculate_profit_margin(self):
        report = FinancialReport.objects.create(
            event_id="event-123",
            total_revenue=Decimal("10000.00"),
            total_expenses=Decimal("3000.00")
        )
        assert report.calculate_profit_margin() == 70.0

    def test_event_id_required(self):
        report = FinancialReport(total_revenue=Decimal("1000.00"))
        with pytest.raises(ValidationError):
            report.full_clean()


@pytest.mark.django_db
class TestRevenueAnalytics:
    def test_create_revenue_analytics(self):
        analytics = RevenueAnalytics.objects.create(
            event_id="event-123",
            ticket_revenue=Decimal("8000.00"),
            sponsorship_revenue=Decimal("2000.00")
        )
        assert analytics.total_revenue == Decimal("10000.00")

    def test_calculate_revenue_breakdown(self):
        analytics = RevenueAnalytics.objects.create(
            event_id="event-123",
            ticket_revenue=Decimal("8000.00"),
            sponsorship_revenue=Decimal("2000.00")
        )
        breakdown = analytics.calculate_revenue_breakdown()
        assert breakdown['ticket_percentage'] == 80.0
        assert breakdown['sponsorship_percentage'] == 20.0
