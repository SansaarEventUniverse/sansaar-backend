from django.urls import path
from presentation.views.health import health_check
from presentation.views.ticket_type_views import (
    create_ticket_type,
    update_ticket_type,
    get_ticket_types,
)
from presentation.views.ticket_views import (
    validate_qr_code,
    check_in_ticket,
    get_ticket,
)
from presentation.views.order_views import (
    CreateOrderView,
    ProcessPurchaseView,
    GetOrderView
)
from presentation.views.promo_code_views import (
    CreatePromoCodeView,
    ValidatePromoCodeView,
    ApplyPromoCodeView
)
from presentation.views.refund_views import (
    RequestRefundView,
    ProcessRefundView,
    GetRefundStatusView
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('events/<str:event_id>/ticket-types/', create_ticket_type, name='create_ticket_type'),
    path('events/<str:event_id>/ticket-types/list/', get_ticket_types, name='get_ticket_types'),
    path('ticket-types/<str:ticket_type_id>/', update_ticket_type, name='update_ticket_type'),
    path('tickets/validate/', validate_qr_code, name='validate_qr_code'),
    path('tickets/<str:ticket_id>/checkin/', check_in_ticket, name='check_in_ticket'),
    path('tickets/<str:ticket_id>/', get_ticket, name='get_ticket'),
    
    # Order endpoints
    path('orders/', CreateOrderView.as_view(), name='create-order'),
    path('orders/<str:order_id>/', GetOrderView.as_view(), name='get-order'),
    path('orders/<str:order_id>/purchase/', ProcessPurchaseView.as_view(), name='process-purchase'),
    
    # Promo code endpoints
    path('events/<str:event_id>/promo-codes/', CreatePromoCodeView.as_view(), name='create-promo-code'),
    path('promo-codes/validate/', ValidatePromoCodeView.as_view(), name='validate-promo-code'),
    path('orders/<str:order_id>/apply-promo/', ApplyPromoCodeView.as_view(), name='apply-promo-code'),
    
    # Refund endpoints
    path('refunds/request/', RequestRefundView.as_view(), name='request-refund'),
    path('refunds/<str:refund_id>/process/', ProcessRefundView.as_view(), name='process-refund'),
    path('refunds/<str:refund_id>/', GetRefundStatusView.as_view(), name='get-refund-status'),
]

