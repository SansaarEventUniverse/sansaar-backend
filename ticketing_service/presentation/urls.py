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
from presentation.views.revenue_views import (
    GetRevenueView,
    GenerateReportView,
    ProcessPayoutView
)
from presentation.views.tax_views import (
    CalculateTaxView,
    GetTaxReportView,
    TaxComplianceView
)
from presentation.views.fraud_views import (
    FraudAlertView,
    SecurityReportView,
    RiskAssessmentView
)
from presentation.views.offline_views import (
    validate_offline,
    sync_ticket_data,
    offline_status
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
    
    # Revenue endpoints
    path('events/<str:event_id>/revenue/', GetRevenueView.as_view(), name='get-revenue'),
    path('events/<str:event_id>/revenue/report/', GenerateReportView.as_view(), name='generate-report'),
    path('events/<str:event_id>/payout/', ProcessPayoutView.as_view(), name='process-payout'),
    
    # Tax endpoints
    path('orders/<str:order_id>/calculate-tax/', CalculateTaxView.as_view(), name='calculate-tax'),
    path('events/<str:event_id>/tax-report/', GetTaxReportView.as_view(), name='get-tax-report'),
    path('events/<str:event_id>/tax-compliance/', TaxComplianceView.as_view(), name='tax-compliance'),
    
    # Fraud detection endpoints
    path('fraud/alerts/', FraudAlertView.as_view(), name='fraud-alerts'),
    path('security/report/', SecurityReportView.as_view(), name='security-report'),
    path('orders/<str:order_id>/risk-assessment/', RiskAssessmentView.as_view(), name='risk-assessment'),
    
    # Offline validation endpoints
    path('validate-offline/', validate_offline, name='validate-offline'),
    path('sync/', sync_ticket_data, name='sync-ticket-data'),
    path('events/<uuid:event_id>/offline-status/', offline_status, name='offline-status'),
]

