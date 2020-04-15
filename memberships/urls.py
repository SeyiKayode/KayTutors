from django.urls import path
from .views import MembershipList, PaymentView, updateTransactions, profile, cancelSubscription
app_name = 'memberships'
urlpatterns = [
    path('', MembershipList.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/', updateTransactions, name='update-transactions'),
    path('profile/', profile, name='profile'),
    path('cancel/', cancelSubscription, name='cancel')
]
