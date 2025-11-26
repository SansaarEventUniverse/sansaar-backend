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

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('wallet/', wallet_payment, name='wallet_payment'),
    path('tickets/<uuid:ticket_id>/add-to-wallet/', add_to_wallet, name='add_to_wallet'),
    path('wallets/<uuid:wallet_id>/status/', wallet_status, name='wallet_status'),
    path('process/', process_payment, name='process_payment'),
    path('<str:payment_id>/refund/', refund_payment, name='refund_payment'),
    path('<str:payment_id>/', get_payment, name='get_payment'),
]
