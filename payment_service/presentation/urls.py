from django.urls import path
from presentation.views.health import health_check
from presentation.views.payment_views import (
    process_payment,
    refund_payment,
    get_payment,
)
from presentation.views.wallet_views import (
    wallet_payment,
    add_to_wallet,
    wallet_status,
)
from presentation.views.subscription_views import (
    CreateSubscriptionView,
    ManageSubscriptionView,
    BillingHistoryView,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    
    # Subscription endpoints (must come before generic payment endpoints)
    path('subscriptions/', CreateSubscriptionView.as_view(), name='subscriptions'),
    path('subscriptions/<uuid:subscription_id>/', ManageSubscriptionView.as_view(), name='manage_subscription'),
    path('subscriptions/<uuid:subscription_id>/billing/', BillingHistoryView.as_view(), name='billing_history'),
    
    # Wallet endpoints
    path('wallet/', wallet_payment, name='wallet_payment'),
    path('tickets/<uuid:ticket_id>/add-to-wallet/', add_to_wallet, name='add_to_wallet'),
    path('wallets/<uuid:wallet_id>/status/', wallet_status, name='wallet_status'),
    
    # Payment endpoints
    path('process/', process_payment, name='process_payment'),
    path('<str:payment_id>/refund/', refund_payment, name='refund_payment'),
    path('<str:payment_id>/', get_payment, name='get_payment'),
]
