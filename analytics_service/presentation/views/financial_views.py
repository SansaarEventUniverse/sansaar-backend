import json
import csv
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from application.services.financial_reporting_service import FinancialReportingService
from application.services.profit_loss_service import ProfitLossService
from domain.models import RevenueAnalytics
from presentation.serializers.financial_serializers import FinancialReportSerializer, RevenueAnalyticsSerializer


class GetFinancialReportView(APIView):
    def get(self, request, event_id):
        service = FinancialReportingService()
        report = service.get_report(event_id)
        return Response(FinancialReportSerializer(report).data)


class RevenueAnalyticsView(APIView):
    def get(self, request, event_id):
        analytics = RevenueAnalytics.objects.get(event_id=event_id)
        return Response(RevenueAnalyticsSerializer(analytics).data)


class ExportFinancialView(APIView):
    def get(self, request, event_id):
        service = ProfitLossService()
        data = service.calculate_profit_loss(event_id)
        return Response(data)


class ExportFinancialCSVView(APIView):
    def get(self, request, event_id):
        service = ProfitLossService()
        data = service.calculate_profit_loss(event_id)
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow({k: str(v) for k, v in data.items()})
        
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="financial_{event_id}.csv"'
        return response
