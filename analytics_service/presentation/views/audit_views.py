from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from domain.models import ComplianceReport
from application.services.audit_trail_service import AuditTrailService
from application.services.audit_reporting_service import AuditReportingService
from presentation.serializers.audit_serializers import (
    AuditTrailSerializer, ComplianceReportSerializer, AuditSearchSerializer
)


class GetAuditTrailView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            service = AuditTrailService()
            trails = service.get_user_audit_trail(user_id)
        else:
            from domain.models import AuditTrail
            trails = AuditTrail.objects.all()
        
        serializer = AuditTrailSerializer(trails, many=True)
        return Response(serializer.data)


class ComplianceReportView(APIView):
    def get(self, request):
        reports = ComplianceReport.objects.all()
        serializer = ComplianceReportSerializer(reports, many=True)
        return Response(serializer.data)


class AuditSearchView(APIView):
    def post(self, request):
        serializer = AuditSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = AuditReportingService()
        results = service.search_audit_trail(serializer.validated_data)
        
        response_serializer = AuditTrailSerializer(results, many=True)
        return Response(response_serializer.data)
