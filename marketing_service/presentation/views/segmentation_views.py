from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.segmentation_service import SegmentationService, AudienceAnalysisService
from presentation.serializers.segmentation_serializers import AudienceSegmentSerializer, AnalyzeAudienceSerializer

@api_view(['GET', 'POST'])
def segment_list_create(request):
    service = SegmentationService()
    
    if request.method == 'GET':
        segments = service.get_segments()
        serializer = AudienceSegmentSerializer(segments, many=True)
        return Response(serializer.data)
    
    serializer = AudienceSegmentSerializer(data=request.data)
    if serializer.is_valid():
        segment = service.create_segment(serializer.validated_data)
        return Response(AudienceSegmentSerializer(segment).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def analyze_audience(request):
    serializer = AnalyzeAudienceSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    service = AudienceAnalysisService()
    result = service.analyze_audience(serializer.validated_data['segment_id'])
    
    return Response(result)
