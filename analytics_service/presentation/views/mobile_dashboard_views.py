from rest_framework.views import APIView
from rest_framework.response import Response
from domain.models import MobileDashboard, MobileWidget
from presentation.serializers.mobile_dashboard_serializers import MobileDashboardSerializer, MobileWidgetSerializer


class GetMobileDashboardView(APIView):
    def get(self, request, dashboard_id):
        dashboard = MobileDashboard.objects.get(id=dashboard_id)
        serializer = MobileDashboardSerializer(dashboard)
        return Response(serializer.data)


class MobileWidgetsView(APIView):
    def get(self, request):
        dashboard_id = request.query_params.get('dashboard_id')
        if dashboard_id:
            widgets = MobileWidget.objects.filter(dashboard_id=dashboard_id)
        else:
            widgets = MobileWidget.objects.all()
        serializer = MobileWidgetSerializer(widgets, many=True)
        return Response(serializer.data)
