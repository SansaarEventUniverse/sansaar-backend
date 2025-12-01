import uuid
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from application.subscription_service import (
    SubscriptionService,
    RecurringPaymentService
)
from presentation.serializers.subscription_serializers import (
    SubscriptionSerializer,
    CreateSubscriptionSerializer,
    ManageSubscriptionSerializer,
    RecurringPaymentSerializer
)


class CreateSubscriptionView(APIView):
    """API view for creating subscriptions."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subscription_service = SubscriptionService()
    
    def post(self, request):
        """Create a new subscription."""
        serializer = CreateSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            subscription = self.subscription_service.create_subscription(
                user_id=serializer.validated_data['user_id'],
                plan_name=serializer.validated_data['plan_name'],
                amount=serializer.validated_data['amount'],
                billing_cycle=serializer.validated_data['billing_cycle']
            )
            
            response_serializer = SubscriptionSerializer(subscription)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """List user subscriptions."""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            subscriptions = self.subscription_service.get_user_subscriptions(
                uuid.UUID(user_id)
            )
            serializer = SubscriptionSerializer(subscriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ValueError:
            return Response(
                {'error': 'Invalid user_id format'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ManageSubscriptionView(APIView):
    """API view for managing subscriptions."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subscription_service = SubscriptionService()
    
    def put(self, request, subscription_id):
        """Manage subscription (pause/cancel)."""
        serializer = ManageSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            action = serializer.validated_data['action']
            
            if action == 'pause':
                subscription = self.subscription_service.pause_subscription(subscription_id)
            elif action == 'cancel':
                subscription = self.subscription_service.cancel_subscription(subscription_id)
            
            response_serializer = SubscriptionSerializer(subscription)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)


class BillingHistoryView(APIView):
    """API view for billing history."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = RecurringPaymentService()
    
    def get(self, request, subscription_id):
        """Get billing history for a subscription."""
        try:
            payments = self.payment_service.get_subscription_payments(subscription_id)
            serializer = RecurringPaymentSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_404_NOT_FOUND)
