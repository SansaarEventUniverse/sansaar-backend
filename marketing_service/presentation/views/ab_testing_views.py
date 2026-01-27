from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from application.services.ab_testing_service import ABTestingService
from presentation.serializers.ab_testing_serializers import ABTestSerializer

@api_view(['GET', 'POST'])
def ab_test_list_create(request):
    service = ABTestingService()
    
    if request.method == 'GET':
        tests = service.get_tests()
        serializer = ABTestSerializer(tests, many=True)
        return Response(serializer.data)
    
    serializer = ABTestSerializer(data=request.data)
    if serializer.is_valid():
        test = service.create_test(serializer.validated_data)
        return Response(ABTestSerializer(test).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def run_ab_test(request, test_id):
    service = ABTestingService()
    test = service.get_test(test_id)
    test.start()
    
    return Response({'status': 'Test started'})
