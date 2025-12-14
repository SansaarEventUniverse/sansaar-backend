import pytest
from decimal import Decimal
from domain.models import FinancialReport, RevenueAnalytics
from infrastructure.repositories.financial_repository import FinancialRepository
from infrastructure.tracking.revenue_tracker import RevenueTracker
from infrastructure.calculation.financial_calculator import FinancialCalculator


@pytest.mark.django_db
class TestFinancialRepository:
    def test_save_financial_report(self):
        repo = FinancialRepository()
        report = repo.save_report("event-123", Decimal("10000.00"), Decimal("3000.00"))
        assert report.net_profit == Decimal("7000.00")

    def test_get_financial_report(self):
        FinancialReport.objects.create(event_id="event-123", total_revenue=Decimal("10000.00"))
        repo = FinancialRepository()
        report = repo.get_report("event-123")
        assert report.event_id == "event-123"


@pytest.mark.django_db
class TestRevenueTracker:
    def test_track_revenue(self):
        tracker = RevenueTracker()
        analytics = tracker.track_revenue("event-123", "ticket", Decimal("5000.00"))
        assert analytics.ticket_revenue == Decimal("5000.00")


@pytest.mark.django_db
class TestFinancialCalculator:
    def test_calculate_metrics(self):
        FinancialReport.objects.create(
            event_id="event-123",
            total_revenue=Decimal("10000.00"),
            total_expenses=Decimal("3000.00")
        )
        calculator = FinancialCalculator()
        metrics = calculator.calculate_metrics("event-123")
        assert metrics['profit_margin'] == 70.0
