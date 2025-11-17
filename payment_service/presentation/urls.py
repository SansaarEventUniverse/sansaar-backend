from django.urls import path
from presentation.views.health import health_check
from presentation.views.payment_views import (
    process_payment,
    refund_payment,
    get_payment,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('process/', process_payment, name='process_payment'),
    path('<str:payment_id>/refund/', refund_payment, name='refund_payment'),
    path('<str:payment_id>/', get_payment, name='get_payment'),
]
