import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from domain.models import FinancialReport, RevenueAnalytics


@pytest.mark.django_db
class TestFinancialReportAPI:
    def test_get_financial_report(self):
        FinancialReport.objects.create(
            event_id="event-123",
            total_revenue=Decimal("10000.00"),
            total_expenses=Decimal("3000.00")
        )
        client = APIClient()
        response = client.get('/api/analytics/events/event-123/financial/')
        assert response.status_code == 200
        assert response.data['net_profit'] == '7000.00'


@pytest.mark.django_db
class TestRevenueAnalyticsAPI:
    def test_get_revenue_analytics(self):
        RevenueAnalytics.objects.create(
            event_id="event-123",
            ticket_revenue=Decimal("8000.00"),
            sponsorship_revenue=Decimal("2000.00")
        )
        client = APIClient()
        response = client.get('/api/analytics/events/event-123/revenue-analytics/')
        assert response.status_code == 200
        assert response.data['total_revenue'] == '10000.00'


@pytest.mark.django_db
class TestFinancialExportAPI:
    def test_export_financial_json(self):
        FinancialReport.objects.create(event_id="event-123", total_revenue=Decimal("10000.00"))
        client = APIClient()
        response = client.get('/api/analytics/events/event-123/financial/export/')
        assert response.status_code == 200

    def test_export_financial_csv(self):
        FinancialReport.objects.create(event_id="event-123", total_revenue=Decimal("10000.00"))
        client = APIClient()
        response = client.get('/api/analytics/events/event-123/financial/export-csv/')
        assert response.status_code == 200
        assert 'text/csv' in response.get('Content-Type', '')
